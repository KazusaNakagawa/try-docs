import glob
from models.excel_mng import ExcelMng


class TestExcelMng(object):

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        print('start')
        cls.files = glob.glob("../zip_storage/*.xlsx")

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        print('end')

    def test_show_row_count_success(self):
        """Success test for number of rows in specified column """
        for file in self.files:
            em = ExcelMng(file)
            count = em.show_row_count(col_name='項目3')
            assert count == 17

    def test_show_row_count_no_column(self):
        """Test when the specified column is missing """
        for file in self.files:
            em = ExcelMng(file)
            count = em.show_row_count(col_name='None_Column')
            assert count is False
