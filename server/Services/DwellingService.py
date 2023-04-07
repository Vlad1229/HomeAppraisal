import psycopg2
from Services.Service import Service


class DwellingService(Service):
    def get_dwellings(self, user_id):
        query = "select * from dwellings where \"UserId\" = %s order by	\"Id\""

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return None
        finally:
            cursor.close()

    def get_dwellings_in_region(self, region_id):
        query = "select * from dwellings where \"RegionId\" = %s order by \"Id\""

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (region_id,))
            rows = cursor.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return None
        finally:
            cursor.close()

    def get_dwelling(self, dwelling_id):
        query = "select * from dwellings where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (dwelling_id,))
            rows = cursor.fetchall()
            if cursor.rowcount == 1:
                for row in rows:
                    return row

            return None
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return None
        finally:
            cursor.close()

    def add_dwelling(self, dwelling_data):
        query = "insert into dwellings (\"UserId\", \"Address\", \"RegionId\", " \
                                       "\"RoomsNum\", \"Size\", \"Floor\", " \
                                       "\"FloorsTotal\", \"Walls\", \"Repair\", " \
                                       "\"Planning\", \"Furniture\", \"Type\", " \
                                       "\"SaleTerm\", \"Cost\", \"IsRelevant\") " \
                                       "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (dwelling_data["user_id"], dwelling_data["address"], dwelling_data["region_id"],
                                   dwelling_data["rooms_num"], dwelling_data["size"], dwelling_data["floor"],
                                   dwelling_data["floors_total"], dwelling_data["walls"], dwelling_data["repair"],
                                   dwelling_data["planning"], dwelling_data["furniture"], dwelling_data["type"],
                                   dwelling_data["sale_term"], dwelling_data["cost"], dwelling_data["is_relevant"]))
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return False
        finally:
            cursor.close()

    def update_dwelling(self, dwelling_data):
        query = "update dwellings set \"Address\" = %s, \"RegionId\" = %s, \"RoomsNum\" = %s, " \
                                      "\"Size\" = %s, \"Floor\" = %s, \"FloorsTotal\" = %s, " \
                                      "\"Walls\" = %s, \"Repair\" = %s, \"Planning\" = %s," \
                                      "\"Furniture\" = %s, \"Type\" = %s, \"SaleTerm\" = %s, " \
                                      "\"Cost\" = %s, \"IsRelevant\" = %s " \
                                      "where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (dwelling_data["address"], dwelling_data["region_id"], dwelling_data["rooms_num"],
                                   dwelling_data["size"], dwelling_data["floor"], dwelling_data["floors_total"],
                                   dwelling_data["walls"], dwelling_data["repair"], dwelling_data["planning"],
                                   dwelling_data["furniture"], dwelling_data["type"], dwelling_data["sale_term"],
                                   dwelling_data["cost"], dwelling_data["is_relevant"], dwelling_data["id"]))
            self.conn.commit()
            cursor.execute("rollback")
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        finally:
            cursor.close()

    def update_dwelling_cost(self, dwelling_id, cost):
        query = "update dwellings set \"Cost\" = %s, \"IsRelevant\" = %s " \
                                      "where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (cost, True, dwelling_id))
            self.conn.commit()
            cursor.execute("rollback")
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return False
        finally:
            cursor.close()

    def delete_dwelling(self, dwelling_id):
        query = "delete from dwellings where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (dwelling_id,))
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return False
        finally:
            cursor.close()
