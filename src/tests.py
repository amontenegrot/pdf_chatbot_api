import unittest

from utilities import get_path


class TestCalculaMedia(unittest.TestCase):
    def test_root_path(self):
        resultado = get_path(1)
        self.assertEqual(
            resultado, 'D:\\Proyectos\\LLMs\\pdf_chatbot_api/'
            )

    def test_current_path(self):
        resultado = get_path()
        self.assertEqual(
            resultado, 'D:\\Proyectos\\LLMs\\pdf_chatbot_api\\src/'
            )

if __name__ == '__main__':
    unittest.main()
