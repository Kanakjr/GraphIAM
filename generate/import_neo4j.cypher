-- empid,firstname,lastname,fullname,userid,department,role,manages,managedby

LOAD CSV WITH HEADERS FROM 'file:///Users.csv' AS row
MERGE (u:User {empId:row.empid, firstname:row.firstname, lastname:row.lastname,
role:row.role,
fullname:row.fullname, email: row.userid})
WITH u, row
UNWIND row.role AS role
MERGE (r:Role {name: role})
MERGE (u)-[s:HAS_ROLE]->(r)
WITH u, row
UNWIND row.department AS department
MERGE (d:Department {name: department})
MERGE (u)-[s:BELONGS_TO]->(d)
WITH u, row
UNWIND row.managedby AS managedby
MATCH (m:User {empId: managedby })
MERGE (u)<-[s:MANAGES]-(m)

