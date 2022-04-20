import mysql.connector

class Repository(object):
    Dk1DB = object
    mycursor = object
    RowsList = []
    # to set connection up as student user on dk1studentuser
    def SetConnection(self):
        self.Dk1DB = mysql.connector.connect(
                  host = "dk1sqlserver.mysql.database.azure.com",
                  user = "dk1student",
                  password = "DKA2022sql",
                  database = "cleverapp"
                  )
        self.mycursor = self.Dk1DB.cursor()


    # to print all table elements
    def GetAll(self, tablename):
        print(self.Dk1DB)
        # mycursor = self.Dk1DB.cursor()
        self.mycursor.execute("select * from " + tablename)
        personResult = self.mycursor.fetchall()
        for x in personResult:
            print(x)



    # add a row to the table.
    def AddRow(self, tablename, disBase, disValue):
        discount =[(disBase, disValue), (disBase, disValue)]
        self.mycursor.execute(" insert into " + tablename + "(discountBase, discountValue) values (%s,%s)", (disBase, disValue) )
        self.Dk1DB.commit()



    # to get all table elements as a list
    def GetAllTolist(self, tablename):
        self.mycursor.execute("select * from " + tablename)
        RowsList = self.mycursor.fetchall()
        return RowsList

    def GetTwoTolist(self, tablename, column1, column2 ):
        self.mycursor.execute("select " + column1 + ", " + column2 + " from " + tablename)
        RowsList = self.mycursor.fetchall()
        return RowsList

    def GetDistinctTolist(self, column, tablename):
        self.mycursor.execute("select distinct " + column + " from " + tablename)
        RowsList = self.mycursor.fetchall()
        return RowsList

    def OverviewOfChargingPointsTolist(self, ConnectorVariantNameId, PostalCode):
        self.mycursor.execute("""SELECT * FROM (SELECT address.LocationName, address.StreetName, address.HouseNumber, address.PostalCode, address.City, charging_type_list.ConnectorVariantName, charging_type_list.Capacity FROM address INNER JOIN charging_type_list ON address.ChargingStationId=charging_type_list.ChargingStationId WHERE charging_type_list.ConnectorVariantName LIKE """ + ConnectorVariantNameId + ") AS table1 WHERE PostalCode like " + "'%" + PostalCode + "%'")
        RowsList = self.mycursor.fetchall()
        return RowsList



#re = Repository()
# re.GetAllTolist(cleverapp.evstats)
#re.SetConnection()
# re.AddRow("discounttable",100000,20)
# print("You made sucess")
