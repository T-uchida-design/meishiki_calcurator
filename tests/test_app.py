import unittest
import json
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page(self):
        """トップページのテスト"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('命式計算', response.data.decode('utf-8'))

    def test_calculate_endpoint(self):
        """計算エンドポイントのテスト"""
        test_data = {
            'birth_date': '2024-03-15',
            'birth_time': '12:00'
        }
        
        response = self.app.post(
            '/calculate',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('wareki', data)

    def test_calculate_invalid_data(self):
        """無効なデータでの計算テスト"""
        test_data = {
            'birth_date': 'invalid-date',
            'birth_time': 'invalid-time'
        }
        
        response = self.app.post(
            '/calculate',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main() 