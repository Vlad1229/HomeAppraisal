import psycopg2
from Services.Service import Service


class RegionService(Service):
    def get_regions(self):
        query = "select * from regions order by	\"Id\""

        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return None
        finally:
            cursor.close()

    def get_region(self, region_id):
        query = "select * from regions where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (region_id,))
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

    def add_region(self, region_data):
        query = "insert into regions (\"RegionName\", \"CrimeRate\", \"River\", " \
                                     "\"NitricOxides\", \"RoomsAverageNumber\", \"TaxRate\", " \
                                     "\"PupilTeacherRatio\", \"LowerStatusPercentage\", " \
                                     "\"RegionCoefficient\") " \
                                     "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (region_data["region_name"], region_data["crime_rate"], region_data["river"],
                                   region_data["nitric_oxides"], region_data["rooms_average_num"], region_data["tax_rate"],
                                   region_data["pupil_teacher_ratio"], region_data["lower_status_percentage"],
                                   region_data["region_coefficient"]))
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return False
        finally:
            cursor.close()

    def update_region(self, region_data):
        query = "update regions set \"RegionName\" = %s, \"CrimeRate\" = %s, \"River\" = %s, " \
                                   "\"NitricOxides\" = %s, \"RoomsAverageNumber\" = %s, \"TaxRate\" = %s, " \
                                   "\"PupilTeacherRatio\" = %s, \"LowerStatusPercentage\" = %s, " \
                                   "\"RegionCoefficient\" = %s " \
                                   "where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (region_data["region_name"], region_data["crime_rate"], region_data["river"],
                                   region_data["nitric_oxides"], region_data["rooms_average_num"], region_data["tax_rate"],
                                   region_data["pupil_teacher_ratio"], region_data["lower_status_percentage"],
                                   region_data["region_coefficient"], region_data["id"]))
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return False
        finally:
            cursor.close()

    def delete_region(self, region_id):
        query = "delete from regions where \"Id\" = %s"

        cursor = self.conn.cursor()
        try:
            cursor.execute(query, (region_id,))
            self.conn.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            cursor.execute("rollback")
            return False
        finally:
            cursor.close()
