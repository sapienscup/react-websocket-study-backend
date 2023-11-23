from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import pprint
pp = pprint.PrettyPrinter(indent=2)


class CassConn:
    def __init__(self) -> None:
        super().__init__()
        auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')
        cluster = Cluster(auth_provider=auth_provider)
        self.session = cluster.connect()


cass = CassConn()

rsp = cass.session.execute("TRUNCATE TABLE software_world.developers_by_language ;")
rsp = cass.session.execute("""
BEGIN BATCH
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (b76485c6-79a9-51b9-b137-b75c718154eb, 'ot@peh.ir', 'arrange', { first_name: 'Ann', last_name: 'Ruiz' });
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (32516d04-c435-53de-8c65-66d56a52e3d1, 'bezo@ik.tw', 'grandmother', { first_name: 'Ivan', last_name: 'Watts' });
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (92210a33-ecf1-5c64-a94a-f62f1212e6b4, 'zo@novkogfa.sm', 'hit', { first_name: 'Brett', last_name: 'Cox' });
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (759a88a8-c37b-5fa7-8415-9eb03c31f686, 'buizabat@zewaz.cy', 'ice', { first_name: 'Ethel', last_name: 'Fleming' });
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (a5aa2d61-4700-5612-bb46-1b842a6448f7, 'jagiv@loaneoc.cm', 'produce', { first_name: 'Victoria', last_name: 'Marshall' });
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (c24529f1-ccad-5536-afea-7ef33f6d0dbb, 'evdoplil@kot.kp', 'nobody', { first_name: 'Josie', last_name: 'Wright' });
INSERT INTO software_world.developers_by_language(id, email, programming_language, name) values (6f52044d-baaf-5fb9-83aa-3ebc4445176a, 'oco@nebhefi.mg', 'taste', { first_name: 'Lizzie', last_name: 'Stokes' });
APPLY BATCH;
""")
