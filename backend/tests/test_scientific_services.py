import io
import os
import sys
import unittest

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.database import SessionLocal
from app.database.models import Report
from app.main import app
from app.routes.protein import parse_protein_sequence
from app.services.ecg_service import ECGService
from app.services.protein_service import ProteinService
from app.services.report_service import ReportService
from app.services.s3_service import S3Service


class ScientificServiceTests(unittest.TestCase):
    def test_ecg_service_analyzes_signal(self):
        service = ECGService()
        csv_text = "ecg\n" + "\n".join(str(value) for value in [0, 0.1, 0.4, 1.2, 0.8, 1.5, 0.3, 0.1, 0.2, 0.9, 1.6, 0.7, 0.2, 0.1, 0.3, 1.1, 0.4, 0.1, 0.2, 0.8, 1.5, 0.5, 0.2, 0.1, 0.15, 1.0, 0.9, 0.8, 0.4, 0.2])
        result = service.analyze_signal(csv_text.encode('utf-8'))

        self.assertIn('heart_rate', result)
        self.assertIn('peak_count', result)
        self.assertIn('classification', result)
        self.assertGreater(result['peak_count'], 0)
        self.assertGreaterEqual(result['heart_rate'], 0)

    def test_protein_service_analyzes_sequence(self):
        service = ProteinService()
        result = service.analyze_sequence('MKTIIALSYIFCLVFADYKDDDDK')

        self.assertEqual(result['sequence_length'], len('MKTIIALSYIFCLVFADYKDDDDK'))
        self.assertGreater(result['molecular_weight'], 0)
        self.assertIn('secondary_structure', result)
        self.assertTrue(result['secondary_structure'])

    def test_protein_parser_ignores_fasta_headers_and_line_endings(self):
        content = b">SampleProtein\r\nMKTIIA LSYI\r\nFCLVFADYKDDDDK\r\n"

        self.assertEqual(parse_protein_sequence(content), 'MKTIIALSYIFCLVFADYKDDDDK')

    def test_s3_service_falls_back_to_local_storage_when_aws_is_not_configured(self):
        service = S3Service()
        target = service.upload_file('local_test.txt', b'cloud test payload', 'tests')

        self.assertTrue(target.startswith('file://'))
        self.assertTrue(target.endswith('/tests/local_test.txt'))
        self.assertIn('local_test.txt', target)

    def test_report_service_generates_live_report_text(self):
        ecg_report = ReportService().generate_ecg_report_text({
            'file_name': 'demo.csv',
            'heart_rate': 74.2,
            'peak_count': 12,
            'mean_value': 0.75,
            'std_value': 0.4,
            'classification': 'Normal sinus rhythm',
        })

        protein_report = ReportService().generate_protein_report_text({
            'protein_name': 'demo_protein.txt',
            'sequence_length': 24,
            'molecular_weight': 2850.4,
            'hydrophobicity': 0.52,
            'secondary_structure': 'Alpha-helix-rich',
        })

        self.assertIn('ECG Analysis Report', ecg_report)
        self.assertIn('Normal sinus rhythm', ecg_report)
        self.assertIn('Protein Analysis Report', protein_report)
        self.assertIn('Alpha-helix-rich', protein_report)

    def test_report_delete_endpoint_removes_unused_report(self):
        db = SessionLocal()
        report = Report(
            report_type='ECG',
            related_id=1,
            file_name='delete_me_report.txt',
            s3_path='file:///tmp/delete_me_report.txt',
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        client = TestClient(app)
        response = client.delete(f'/api/reports/{report.id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Report deleted successfully')
        self.assertIsNone(db.query(Report).filter(Report.id == report.id).first())
        db.close()


if __name__ == '__main__':
    unittest.main()
