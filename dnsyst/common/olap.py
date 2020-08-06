import os
import clr

dirname = os.path.dirname(__file__)
dll_path = 'dll/Microsoft.AnalysisServices.AdomdClient.dll'

clr.AddReference (os.path.join(dirname, dll_path))
clr.AddReference ('System.Data')

from System.Data import DataSet
from Microsoft.AnalysisServices.AdomdClient import (
                                            AdomdConnection, 
                                            AdomdDataAdapter
                                            )

import pandas as pd

class SSAS:
    def __init__(self, params):
        """
        args:
            params (str): connection params. 
            Examp: 'Data Source=dwh;Catalog=DNS-OLAP;'
        """
        self.conn = AdomdConnection(params)
        self.conn.Open()

    def _to_pd(self, DataTable):
        """
        args:
            DataTable (System.Data.DataTable .NET object): .net table format.
                see .NET Core docs: https://docs.microsoft.com/ru-ru/dotnet/api/system.data.datatable?view=netcore-3.1

        """
        col_name = []
        rows = []

        #list of System.Data.DataColumn objects
        data_col = list(DataTable.Columns)
        #list of System.Data.DataRow objects
        data_row = list(DataTable.Rows)

        for col in data_col:
            col_name.append(col.ColumnName)

        for row in data_row:
            row_values = list(row.ItemArray)
            rows.append(row_values)

        return pd.DataFrame(rows, columns=col_name)

    def execute(self, query):
        """

        """
        comnd = self.conn.CreateCommand()
        comnd.CommandText = query
        adp = AdomdDataAdapter(comnd)

        set_param =  DataSet()
        adp.Fill(set_param)

        return self._to_pd(set_param.Tables[0])

    def close(self):
        self.conn.Close()