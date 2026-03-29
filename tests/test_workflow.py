import unittest
from src.workflow import workflow

class TestWorkflow(unittest.TestCase):
    def test_workflow_initialization(self):
        """测试工作流初始化"""
        self.assertIsNotNone(workflow)
    
    def test_run_method_exists(self):
        """测试run方法存在"""
        self.assertTrue(hasattr(workflow, 'run'))

if __name__ == '__main__':
    unittest.main()