# encoding: utf8
import pyodbc
import arcpy
import os


all_select_fields = [
    ("t.ID_ADR", '"ID_ADR"', True, "DOUBLE"),
    ("t.ADR_NUM", '"ADR_NUM"', True, "DOUBLE"),
    ("r1.UIDREGION", '"UIDREGION"', True, "DOUBLE"),
    ("r1.NAMEOBJECT", '"REGION"', True, "TEXT"),
    ("r2.OBJECTNUMBER", '"DISTR_ID"', True, "DOUBLE"),
    ("r2.UIDDISTR", '"UIDDISTR"', True, "DOUBLE"),
    ("r2.NAMEOBJECT", '"DISTR"', True, "TEXT"),
    ("r3.OBJECTNUMBER", '"SELSS_ID"', True, "DOUBLE"),
    ("r3.NAMEOBJECT", '"SELSS_NAME"', True, "TEXT"),
    ("p1.CATEGORY", '"CATEGORY"', True, "DOUBLE"),
    ("p1.NAME", '"NAME"', True, "TEXT"),
    ("p1.SHORTNAME", '"SHORTNAME"', True, "TEXT"),
    ("v.NAME", '"CATEGORY_ATE"', True, "TEXT"),
    ("r4.OBJECTNUMBER", '"ID_ATE"', True, "DOUBLE"),
    ("r4.NAMEOBJECT", '"NAME_ATE"', True, "TEXT"),
    ("c.IAEUID", '"ID_EVA"', True, "DOUBLE"),
    ("c.ELEMENTTYPE", '"ELEMENTTYP"', True, "DOUBLE"),
    ("c.ELEMENTTYPENAME", '"ELTYPENAME"', True, "TEXT"),
    ("spr.SHORTNAME_RUS", '"SHORTNAMEV"', True, "TEXT"),
    ("c.ELEMENTNAME", '"ELEMENTNAM"', True, "TEXT"),
    ("t.PROP_TYPE", '"PROP_TYPE"', True, "DOUBLE"),
    ("k.NUM_HOUSE", '"NUM_HOUSE"', True, "DOUBLE"),
    ("k.NUM_CORP", '"NUM_CORP"', True, "TEXT"),
    ("k.IND_HOUSE", '"IND_HOUSE"', True, "TEXT"),
    ("k.NUM_ROOM", '"NUM_ROOM"', True, "DOUBLE"),
    ("k.IND_ROOM", '"IND_ROOM"', True, "TEXT"),
    ("k.KM", '"KM"', True, "TEXT"),
    ("t.REMARK", '"REMARK"', True, "TEXT"),
    ("e.INDEXES", '"INDEXES"', True, "TEXT"),
    ("s.NAME",'"ADR_STATUS"', True, "TEXT"),
    ("z.DATE_REG", '"DATE_REG"', True, "DATE"),
    ("t.BCOORD", '"BCOORD"', True, "DOUBLE"),
    ("t.LCOORD", '"LCOORD"', True, "DOUBLE")
]


prop_type = (('ЗУ', 1, True),
             ('КС', 2, True),
             ('НЗКС', 4, False),
             ('ИП', 8, False))


sk_42 = "GEOGCS['GCS_Pulkovo_1942',DATUM['D_Pulkovo_1942',SPHEROID['Krasovsky_1940',6378245.0,298.3]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.9830007334435E-09;0.001;0.001;IsHighPrecision"
wgs84 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
regions = {"Брестская": 1, "Витебская": 2, "Гомельская": 3, "Гродненская": 4, "Минская": 6, "Могилевская": 7}
districts = {'Барановичский': 104,  'Берёзовский': 108,  'Брестский': 112,  'Ганцевичский': 116,  'Дрогичинский': 120,  'Жабинковский': 125,  'Ивановский': 130,  'Ивацевичский': 134,  'Каменецкий': 140,  'Кобринский': 143,  'Лунинецкий': 147,  'Ляховичский': 150,  'Малоритский': 152,  'Пинский': 154,  'Пружанский': 156,  'Столинский': 158,  'Бешенковичский': 205,  'Браславский': 208,  'Верхнедвинский': 210,  'Витебский': 212,  'Глубокский': 215,  'Городокский': 218,  'Докшицкий': 221,  'Дубровенский': 224,  'Лепельский': 227,  'Лиозненский': 230,  'Миорский': 233,  'Оршанский': 236,  'Полоцкий': 238,  'Поставский': 240,  'Россонский': 242,  'Сенненский': 244,  'Толочинский': 246,  'Ушачский': 249,  'Чашникский': 251,  'Шарковщинский': 255,  'Шумилинский': 258,  'Брагинский': 303,  'Буда-Кошелевский': 305,  'Ветковский': 308,  'Гомельский': 310,  'Добрушский': 312,  'Ельский': 314,  'Житковичский': 316,  'Жлобинский': 318,  'Калинковичский': 323,  'Кормянский': 325,  'Лельчицкий': 328,  'Лоевский': 330,  'Мозырский': 335,  'Наровлянский': 338,  'Октябрьский': 340,  'Петриковский': 343,  'Речицкий': 345,  'Рогачёвский': 347,  'Светлогорский': 350,  'Хойникский': 354,  'Чечерский': 356,  'Берестовицкий': 404,  'Волковысский': 408,  'Вороновский': 413,  'Гродненский': 420,  'Дятловский': 423,  'Зельвенский': 426,  'Ивьевский': 429,  'Кореличский': 433,  'Лидский': 436,  'Мостовский': 440,  'Новогрудский': 443,  'Островецкий': 446,  'Ошмянский': 449,  'Свислочский': 452,  'Слонимский': 454,  'Сморгонский': 456,  'Щучинский': 458,  'Березинский': 604,  'Борисовский': 608,  'Вилейский': 613,  'Воложинский': 620,  'Дзержинский': 622,  'Клецкий': 625,  'Копыльский': 628,  'Крупский': 630,  'Логойский': 632,  'Любанский': 634,  'Минский': 636,  'Молодечненский': 638,  'Мядельский': 640,  'Несвижский': 642,  'Пуховичский': 644,  'Слуцкий': 646,  'Смолевичский': 648,  'Солигорский': 650,  'Стародорожский': 652,  'Столбцовский': 654,  'Узденский': 656,  'Червенский': 658,  'Белыничский': 704,  'Бобруйский': 708,  'Быховский': 713,  'Глусский': 717,  'Горецкий': 720,  'Дрибинский': 723,  'Кировский': 725,  'Климовичский': 728,  'Кличевский': 730,  'Костюковичский': 735,  'Краснопольский': 738,  'Кричевский': 740,  'Круглянский': 742,  'Могилевский': 744,  'Мстиславский': 746,  'Осиповичский': 748,  'Славгородский': 750,  'Хотимский': 752,  'Чаусский': 754,  'Чериковский': 756,  'Шкловский': 758}


class AddressClient(object):
    """
    Create file access with two tables: attributes data about address and coordinates (if necessary). It create table on district/region/capital.
    """
    def __init__(self, name_territory, work_path, name_file, name_table, path_to_maska, login, password, select_fields=all_select_fields, prop_type=prop_type):

        self.region = False
        self.district = False
        self.minsk = False
        self.name_territory = name_territory
        self.with_coord = False
        self.work_path = work_path
        self.name_file = name_file
        self.name_table = name_table
        self.path_to_maska = path_to_maska
        self.login = login
        self.password = password
        self.select_fields = select_fields
        self.prop_type = prop_type
        self.create_address_layer()

    def create_select_fields(self):
        """
        func create str from list select_fields
        :return: str select fields, which will be use in func select quiryset in DateBase
        """
        select_fields_list = []
        for field in self.select_fields:
            if field[2]:
                select_fields_list.append(field[0]+ " AS "+field[1]+",")
        return ' '.join(select_fields_list)[:-1]

    def create_select_prop_type(self):
        """
        create tuple of prop_type КС/НЗКС/ЗУ/ИП
        :return:
        """
        list_prop_type = []
        for type in self.prop_type:
            if type[2]:
                list_prop_type.append(type[1])
        if len(list_prop_type)>1:
            return "IN {0}".format(tuple(list_prop_type))
        else:
            return "= {0}".format(list_prop_type[0])

    def set_with_coord(self):
        """
        func definition existence of coordinate among last two fields in queryset
        :return: indication of existence of coordinate - True/False
        """
        for field in self.select_fields[-2:]:
            if field[0].find("COORD") > -1 and field[2]:
                self.with_coord = True
                break
        return self.with_coord

    def choose_territory(self):
        """
        func definition territory Minsk/Region/District
        :return: dict territory like {minsk: False, region: False, district: True}
        """
        if self.name_territory == 'Минск':
            self.minsk = True
        else:
            for region in regions:
                if self.name_territory == region:
                    self.region = True
        if not self.minsk and not self.region:
            self.district = True
        return {"minsk": self.minsk, "region": self.region, "district": self.district}

    def create_address_region_queryset(self):
        """
        select address on REGION from DateBase Reestr Address
        :return: queryset address on REGION
        """
        # Connect to DataBase Reestr Address
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login + ";PWD=" + self.password)
        cursor = conn.cursor()
        # SQL expression
        expression = """SELECT {0}

FROM     
ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTs i, RADR.GROUNDS z, RADR.OPER b, ATEREESTR.X_ATEREGION g, RADR.TYPE_SPECIF s, RADR.REF_INADR d,     

ATEREESTR.ATEOBJECT r

left JOIN (SELECT * from ATEREESTR.ATEOBJECT obl where obl.CATEGORY=101 
AND obl.UIDOPERIN = (SELECT MAX (obl1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT obl1    
WHERE obl.OBJECTNUMBER=obl1.OBJECTNUMBER 
GROUP BY obl.OBJECTNUMBER)) r1 on SUBSTR (r.SOATO, 1, 1) = SUBSTR (r1.SOATO, 1, 1)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT distr where distr.CATEGORY =102  
AND   distr.UIDOPERIN=( SELECT MAX (distr1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT distr1    
WHERE distr.OBJECTNUMBER=distr1.OBJECTNUMBER
GROUP BY distr.OBJECTNUMBER)) r2  on SUBSTR (r2.SOATO, 1, 4)=SUBSTR (r.SOATO, 1, 4)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT ss where ss.CATEGORY =103     
AND ss.UIDOPERIN=( SELECT MAX (ss1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT ss1    
WHERE ss.OBJECTNUMBER=ss1.OBJECTNUMBER
GROUP BY ss.OBJECTNUMBER)) r3 on SUBSTR (r.SOATO, 1, 7) = SUBSTR (r3.SOATO, 1, 7)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT np where np.CATEGORY < 240 and np.CATEGORY > 103 AND np.UIDOPERIN=( SELECT MAX (np1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT np1   
WHERE np.OBJECTNUMBER=np1.OBJECTNUMBER
GROUP BY np.OBJECTNUMBER)) r4 on r4.OBJECTNUMBER = r.OBJECTNUMBER

left JOIN ATEREESTR.X_ATECATEGORY p1 on r4.CATEGORY = p1.CATEGORY
left JOIN ATEREESTR.X_ATEVALUE v on r4.ATEVALUE = v.ATEVALUE,

RADR.ADDRESSES t    
left JOIN RADR.INDEXES e ON t.ID_INDEX=e.ID_INDEX,    
RADR.INTERNAL_ADR k    
Left JOIN (SELECT * FROM IAE.ADRELEMENTS c1     
WHERE  c1.JRNREG_IN = (SELECT MAX (c2.JRNREG_IN)    
FROM IAE.ADRELEMENTS c2    
WHERE c1.IAEUID = c2.IAEUID AND  c1.IAEUID NOT in (28170, 56753, 35618, 35592) 
GROUP BY c2.IAEUID)) c ON k.ID_EVA = c.IAEUID
 
left JOIN NKA_SPR.X_EVA_TYPES_ADDR spr on spr.CODE_1=c.ELEMENTTYPE

WHERE
r.UIDOPERIN = (SELECT MAX (r5.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT r5    
WHERE r.OBJECTNUMBER=r5.OBJECTNUMBER    
GROUP BY R5.OBJECTNUMBER) 

AND  
 t.ID_ADR = (SELECT max (ad.ID_ADR)  
from RADR.ADDRESSES ad   WHERE t.ID_ADR=ad.ID_ADR GROUP BY ad.ADR_NUM)
AND  t.ID_ADR= d.ID_ADR AND k.ID_IN_ADR=d.ID_IN_ADR AND t.PROP_TYPE {1} AND t.ACTUAL is null  AND t.OBJ_ID=r.OBJECTNUMBER AND  p.CATEGORY=r.CATEGORY AND i.UIDDISTR=r.UIDDISTR  AND g.UIDREGION=r.UIDREGION AND  s.ID_SPEC=t.KOD_SPEC AND t.OPER_IN=b.ID_OPER AND z.ID_GR=b.ID_GR AND  d.OPER_OUT  is null AND r.OBJECTNUMBER<>17030 AND r.UIDREGION={2}
    
order by  r1.UIDREGION, r2.UIDDISTR, r3.NAMEOBJECT,  p1.SHORTNAME, r4.NAMEOBJECT, c.ELEMENTTYPE, c.ELEMENTNAME, k.NUM_HOUSE, k.NUM_CORP, k.IND_HOUSE,  t.PROP_TYPE, k.NUM_ROOM, k.IND_ROOM, k.KM
""".format(self.create_select_fields(), self.create_select_prop_type(), regions[self.name_territory])
        cursor.execute(expression)
        return cursor.fetchall()

    def create_address_district_queryset(self):
        """
        select address on DISTRICT from DateBase Reestr Address
        :return: queryset address on DISTRICT
        """
        # Connect to DataBase Reestr Address

        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login + ";PWD=" + self.password)
        cursor = conn.cursor()
        # SQL expression
        expression = """
        SELECT {0}

FROM     
ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTs i, RADR.GROUNDS z, RADR.OPER b, ATEREESTR.X_ATEREGION g, RADR.TYPE_SPECIF s, RADR.REF_INADR d,     

ATEREESTR.ATEOBJECT r

left JOIN (SELECT * from ATEREESTR.ATEOBJECT obl where obl.CATEGORY=101 
AND obl.UIDOPERIN = (SELECT MAX (obl1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT obl1    
WHERE obl.OBJECTNUMBER=obl1.OBJECTNUMBER 
GROUP BY obl.OBJECTNUMBER)) r1 on SUBSTR (r.SOATO, 1, 1) = SUBSTR (r1.SOATO, 1, 1)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT distr where distr.CATEGORY =102  
AND   distr.UIDOPERIN=( SELECT MAX (distr1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT distr1    
WHERE distr.OBJECTNUMBER=distr1.OBJECTNUMBER
GROUP BY distr.OBJECTNUMBER)) r2  on SUBSTR (r2.SOATO, 1, 4)=SUBSTR (r.SOATO, 1, 4)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT ss where ss.CATEGORY =103     
AND ss.UIDOPERIN=( SELECT MAX (ss1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT ss1    
WHERE ss.OBJECTNUMBER=ss1.OBJECTNUMBER
GROUP BY ss.OBJECTNUMBER)) r3 on SUBSTR (r.SOATO, 1, 7) = SUBSTR (r3.SOATO, 1, 7)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT np where np.CATEGORY < 240 and np.CATEGORY > 103 AND np.UIDOPERIN=( SELECT MAX (np1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT np1   
WHERE np.OBJECTNUMBER=np1.OBJECTNUMBER
GROUP BY np.OBJECTNUMBER)) r4 on r4.OBJECTNUMBER = r.OBJECTNUMBER

left JOIN ATEREESTR.X_ATECATEGORY p1 on r4.CATEGORY = p1.CATEGORY
left JOIN ATEREESTR.X_ATEVALUE v on r4.ATEVALUE = v.ATEVALUE,

RADR.ADDRESSES t    
left JOIN RADR.INDEXES e ON t.ID_INDEX=e.ID_INDEX,    
RADR.INTERNAL_ADR k    
Left JOIN (SELECT * FROM IAE.ADRELEMENTS c1     
WHERE  c1.JRNREG_IN = (SELECT MAX (c2.JRNREG_IN)    
FROM IAE.ADRELEMENTS c2    
WHERE c1.IAEUID = c2.IAEUID AND  c1.IAEUID NOT in (28170, 56753, 35618, 35592) 
GROUP BY c2.IAEUID)) c ON k.ID_EVA = c.IAEUID
 
left JOIN NKA_SPR.X_EVA_TYPES_ADDR spr on spr.CODE_1=c.ELEMENTTYPE

WHERE
r.UIDOPERIN = (SELECT MAX (r5.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT r5    
WHERE r.OBJECTNUMBER=r5.OBJECTNUMBER    
GROUP BY R5.OBJECTNUMBER) 

AND  
 t.ID_ADR = (SELECT max (ad.ID_ADR)  
from RADR.ADDRESSES ad   WHERE t.ID_ADR=ad.ID_ADR GROUP BY ad.ADR_NUM)
AND  t.ID_ADR= d.ID_ADR AND k.ID_IN_ADR=d.ID_IN_ADR AND t.PROP_TYPE {1} AND t.ACTUAL is null  AND t.OBJ_ID=r.OBJECTNUMBER AND  p.CATEGORY=r.CATEGORY AND i.UIDDISTR=r.UIDDISTR  AND g.UIDREGION=r.UIDREGION AND  s.ID_SPEC=t.KOD_SPEC AND t.OPER_IN=b.ID_OPER AND z.ID_GR=b.ID_GR AND  d.OPER_OUT  is null AND r.OBJECTNUMBER<>17030 AND r.UIDDISTR={2}
    
order by  r1.UIDREGION, r2.UIDDISTR, r3.NAMEOBJECT,  p1.SHORTNAME, r4.NAMEOBJECT, c.ELEMENTTYPE, c.ELEMENTNAME, k.NUM_HOUSE, k.NUM_CORP, k.IND_HOUSE,  t.PROP_TYPE, k.NUM_ROOM, k.IND_ROOM, k.KM

        """.format(self.create_select_fields(), self.create_select_prop_type(), districts[self.name_territory])
        cursor.execute(expression)
        return cursor.fetchall()

    def create_address_minsk_queryset(self):
        """
        select address on MINSK from DateBase Reestr Address
        :return: queryset address on MINSK
        """
        # Connect to DataBase Reestr Address
        conn = pyodbc.connect(
            "DRIVER={Oracle in OraClient10g_home1};DBQ=NCABASE:1521/WIN.MINSK.NCA;UID=" + self.login + ";PWD=" + self.password)
        cursor = conn.cursor()
        # SQL expression
        expression = """
        SELECT {0}

FROM     
ATEREESTR.X_ATECATEGORY p, ATEREESTR.X_ATEDISTRICTs i, RADR.GROUNDS z, RADR.OPER b, ATEREESTR.X_ATEREGION g, RADR.TYPE_SPECIF s, RADR.REF_INADR d,     

ATEREESTR.ATEOBJECT r

left JOIN (SELECT * from ATEREESTR.ATEOBJECT obl where obl.CATEGORY=101 
AND obl.UIDOPERIN = (SELECT MAX (obl1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT obl1    
WHERE obl.OBJECTNUMBER=obl1.OBJECTNUMBER 
GROUP BY obl.OBJECTNUMBER)) r1 on SUBSTR (r.SOATO, 1, 1) = SUBSTR (r1.SOATO, 1, 1)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT distr where distr.CATEGORY =102  
AND   distr.UIDOPERIN=( SELECT MAX (distr1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT distr1    
WHERE distr.OBJECTNUMBER=distr1.OBJECTNUMBER
GROUP BY distr.OBJECTNUMBER)) r2  on SUBSTR (r2.SOATO, 1, 4)=SUBSTR (r.SOATO, 1, 4)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT ss where ss.CATEGORY =103     
AND ss.UIDOPERIN=( SELECT MAX (ss1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT ss1    
WHERE ss.OBJECTNUMBER=ss1.OBJECTNUMBER
GROUP BY ss.OBJECTNUMBER)) r3 on SUBSTR (r.SOATO, 1, 7) = SUBSTR (r3.SOATO, 1, 7)

left JOIN (SELECT * from ATEREESTR.ATEOBJECT np where np.CATEGORY < 240 and np.CATEGORY > 103 AND np.UIDOPERIN=( SELECT MAX (np1.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT np1   
WHERE np.OBJECTNUMBER=np1.OBJECTNUMBER
GROUP BY np.OBJECTNUMBER)) r4 on r4.OBJECTNUMBER = r.OBJECTNUMBER

left JOIN ATEREESTR.X_ATECATEGORY p1 on r4.CATEGORY = p1.CATEGORY
left JOIN ATEREESTR.X_ATEVALUE v on r4.ATEVALUE = v.ATEVALUE,

RADR.ADDRESSES t    
left JOIN RADR.INDEXES e ON t.ID_INDEX=e.ID_INDEX,    
RADR.INTERNAL_ADR k    
Left JOIN (SELECT * FROM IAE.ADRELEMENTS c1     
WHERE  c1.JRNREG_IN = (SELECT MAX (c2.JRNREG_IN)    
FROM IAE.ADRELEMENTS c2    
WHERE c1.IAEUID = c2.IAEUID AND  c1.IAEUID NOT in (28170, 56753, 35618, 35592) 
GROUP BY c2.IAEUID)) c ON k.ID_EVA = c.IAEUID
 
left JOIN NKA_SPR.X_EVA_TYPES_ADDR spr on spr.CODE_1=c.ELEMENTTYPE

WHERE
r.UIDOPERIN = (SELECT MAX (r5.UIDOPERIN)    
FROM ATEREESTR.ATEOBJECT r5    
WHERE r.OBJECTNUMBER=r5.OBJECTNUMBER    
GROUP BY R5.OBJECTNUMBER) 

AND  
 t.ID_ADR = (SELECT max (ad.ID_ADR)  
from RADR.ADDRESSES ad   WHERE t.ID_ADR=ad.ID_ADR GROUP BY ad.ADR_NUM)
AND  t.ID_ADR= d.ID_ADR AND k.ID_IN_ADR=d.ID_IN_ADR AND t.PROP_TYPE {1} AND t.ACTUAL is null  AND t.OBJ_ID=r.OBJECTNUMBER AND  p.CATEGORY=r.CATEGORY AND i.UIDDISTR=r.UIDDISTR  AND g.UIDREGION=r.UIDREGION AND  s.ID_SPEC=t.KOD_SPEC AND t.OPER_IN=b.ID_OPER AND z.ID_GR=b.ID_GR AND  d.OPER_OUT  is null AND r.OBJECTNUMBER=17030
    
order by  r1.UIDREGION, r2.UIDDISTR, r3.NAMEOBJECT,  p1.SHORTNAME, r4.NAMEOBJECT, c.ELEMENTTYPE, c.ELEMENTNAME, k.NUM_HOUSE, k.NUM_CORP, k.IND_HOUSE,  t.PROP_TYPE, k.NUM_ROOM, k.IND_ROOM, k.KM
""".format(self.create_select_fields(), self.create_select_prop_type())
        cursor.execute(expression)
        return cursor.fetchall()


    def create_address_layer(self):
        """
        :return:
        """
        # Choose territory and select qyeryset
        self.choose_territory()
        if self.region:
            queryset = self.create_address_region_queryset()
        elif self.minsk:
            queryset = self.create_address_minsk_queryset()
        else:
            queryset = self.create_address_district_queryset()

        # create mdb

        try:
            arcpy.CreatePersonalGDB_management(self.work_path, self.name_file)

        except:
            pass
        self.nameDateBase = os.path.join(self.work_path, self.name_file)
        # Create table in DataBase
        arcpy.CreateTable_management(self.nameDateBase, self.name_table, "", "")
        name_table = os.path.join(self.nameDateBase, self.name_table)
        # Create fields in table
        list_field = []
        # Call function set_with_coord() at first time
        if self.set_with_coord():
            select_field = self.select_fields[:-2]
        else:
            select_field = self.select_fields
        for field in select_field:
            # field[2] is means True/False in all_select_fields
            if field[2]:
                # FIELDS: field[1][1:-1] - is allies for field like 'ID_ATE', so we cut '', field[3] - type of field like text or double
                arcpy.AddField_management(name_table, field[1][1:-1], field[3], "", "", "", "", "NULLABLE","NON_REQUIRED", "")
                list_field.append(field[1][1:-1])
        if self.with_coord:
            cursor_arc = arcpy.da.InsertCursor(name_table, list_field)
            for element in queryset:
                cursor_arc.insertRow(element[:-2])
        # this case if select doesn't contain coordinates, another words self.with_coord = False
        else:
            cursor_arc = arcpy.da.InsertCursor(name_table, list_field)
            for element in queryset:
                cursor_arc.insertRow(element)

        # if queryset contains coordinates we create shp address and convert it in wgs84
        if self.with_coord:
            # create mdb
            # Add values in SHP address42
            arcpy.CreateFeatureclass_management(self.work_path, "address42.shp", 'POINT', "", "DISABLED", "DISABLED", sk_42, "", "0", "0", "0")
            name_address42 = os.path.join(self.work_path, "address42.shp")

            name_address = os.path.join(self.work_path, '{0}_address.shp'.format(self.name_table))
            arcpy.AddField_management(name_address42, "ID_ADR", "LONG", "", "", "", "", "NULLABLE", "REQUIRED", "")
            cursor_arc = arcpy.da.InsertCursor(name_address42, ["ID_ADR", "SHAPE@XY"])
            for element in queryset:
                if element[-1] is not None:
                    cursor_arc.insertRow([element[0]] + [(element[-1], element[-2])])
            # convert coordinates from sk42 to wgs84
            arcpy.Project_management(name_address42, name_address, wgs84, "CK42_to_ITRF2005", sk_42)
            # add coordinates in wgs84
            arcpy.AddXY_management(name_address)
            # Delete shp address42
            arcpy.Delete_management(name_address42, "FeatureClass")

            maska_temp = os.path.join(self.path_to_maska, 'maska_temp.shp')

            if self.region:
                arcpy.Select_analysis(os.path.join(self.path_to_maska, "region_maska84.shp"), maska_temp, "\"uid\" = {0}".format(regions[self.name_territory]))
            elif self.minsk:
                arcpy.Select_analysis(os.path.join(self.path_to_maska, "region_maska84.shp"), maska_temp, "\"uid\" = 5")
            else:
                arcpy.Select_analysis(os.path.join(self.path_to_maska, "district_maska84.shp"), maska_temp, "\"uid\" = {0}".format(districts[self.name_territory]))

            arcpy.Clip_analysis(name_address, maska_temp, os.path.join(self.nameDateBase, '{0}_address'.format(self.name_table)), "")

            # arcpy.FeatureClassToGeodatabase_conversion(name_address, self.nameDateBase)
            arcpy.Delete_management(name_address, "FeatureClass")
            arcpy.Delete_management(maska_temp, "FeatureClass")
