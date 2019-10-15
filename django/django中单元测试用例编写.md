## 常规测试用例编写
```python 
import unittest


class Demo():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self):

        return self.x + self.y

    def sub(self):
        return self.x - self.y


class DemoTest(unittest.TestCase):

    def setUp(self):
        """测试之前的准备工作"""
        self.nu = Demo(2, 3)
        pass

    def tearDown(self):
        """测试之后的收尾工作"""
        pass

    def test_add(self):
        ret = self.nu.add()
        self.assertEqual(ret, 5)

    def test_sub(self):
        ret = self.nu.sub()
        self.assertEqual(ret, -1)


if __name__ == "__main__":
    # 狗仔测试集合
    suite = unittest.TestSuite()
    suite.addTest(DemoTest("test_add"))
    suite.addTest(DemoTest("test_sub"))

    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
```
## 在django中使用单元测试 
```python
from django.test import TestCase
from app02.models import Student
# Create your tests here.
# 测试model
class StudentTest(TestCase):
    
    def setUp(self):
        Student.objects.create(name='签到哥', age=18)

    def test_student_create(self):
        obj = Student.objects.get(name='签到哥')
        self.assertEqual(obj.age, 18)
class HomeTest(TestCase):

    def test_home_page_renders_home_template(self):
        """测试index视图"""
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '箭头函数.html')  # 判断使用的模板文件
```
然后运行 `python manage.py test`