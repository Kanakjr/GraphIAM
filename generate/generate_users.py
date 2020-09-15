import collections
import csv
import json
import random
from faker import Faker
import config

#Import necessary  config data
fake_users_count         = config.fake_users_count
csv_file                 = config.csv_file
csv_columns              = config.csv_columns
domain                   = config.domain
departments              = config.departments
departments_distrib      = config.departments_distrib
departments_distrib_dict = config.departments_distrib_dict
roles                    = config.roles
roles_limit              = config.roles_limit
roles_assigned           = []
manages                  = config.manages
profiles_lst             = {}

fake = Faker('en_IN')

def partition (list_in, n):
    random.shuffle(list_in)
    return [list_in[i::n] for i in range(n)]

def gen_department():
    return random.choice(departments)

def gen_role(department):
    for role,limit in roles_limit.items():
        if role in roles[department]: 
            if limit>0:
                roles_limit[role]=roles_limit[role]-1
                return role
            elif limit==0:
                roles_assigned.append(role)
    role_choices = set(roles[department])-set(roles_assigned)
    return random.choice(list(role_choices))

for dept,dist in zip(departments,departments_distrib):
    dept_users_count = int(fake_users_count*dist/100)
    #print(dept,dept_users_count)
    for _ in range(dept_users_count):
        firstname  = fake.first_name()
        lastname   = fake.last_name()
        fullname   = firstname+' '+lastname
        userid     = str.lower(firstname+'_'+lastname+'@'+domain)
        empid      = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
        #birthdate  = fake.date_of_birth()
        department = dept #gen_department()
        role       = gen_role(department)
        profile = {'firstname':firstname,'lastname':lastname,'fullname':fullname,
        'userid':userid,'empid':empid,
        #'birthdate':birthdate,
        'department':department,'role':role
        ,'managedby':[]
        }
        profiles_lst[empid] = profile

print(f'Generated {len(profiles_lst)} number of profiles')
profiles_lst_dept = [value["department"] for key,value in profiles_lst.items()]
profiles_lst_roles = [value["role"] for key,value in profiles_lst.items()]
print(f'\nDepartment: {collections.Counter(profiles_lst_dept).most_common()}')
print(f'\nRoles: {collections.Counter(profiles_lst_roles).most_common()}')
print('')

for manages,managedby in manages.items():
    manages_user_lst = []
    managedby_user_lst = []
    for empid,p in profiles_lst.items():
        if p['role'] == manages:
            manages_user_lst.append(p['empid'])
        elif p['role'] in managedby:
            managedby_user_lst.append(p['empid'])
    count_manages = len(manages_user_lst)
    count_managedby = len(managedby_user_lst)
    print(count_manages,manages,'-- manages ->',count_managedby,managedby)

    partition_managedby_user_lst = partition(managedby_user_lst,len(manages_user_lst))
    
    for m,mb_lst in zip(manages_user_lst,partition_managedby_user_lst):
        for mb in mb_lst:
            #profiles_lst[m]['manages'].append(mb)
            profiles_lst[mb]['managedby'].append(m)
            #print(m,mb)

# with open('users.json', 'w') as fp: json.dump(profiles_lst, fp)

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for empid,data in profiles_lst.items():
            #data['manages'] = ';'.join(data['manages'])
            data['managedby'] = ';'.join(data['managedby'])
            writer.writerow(data)
except IOError:
    print("I/O error")
