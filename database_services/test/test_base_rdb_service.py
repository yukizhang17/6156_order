from base_rdb_service import BaseDataResource

def t1():

    res = BaseDataResource.get_by_prefix(
        "users", "user", "name_first", "Yuki"
    )
    print("t1 resule = ", res)


def t2():

    res = BaseDataResource.find_by_template(
        "users", "user", {"name_last": "Zhang"}, None
    )
    print("t2 resuls = ", res)


def t3():

    res = BaseDataResource.create(
        "users", "user",
            {
                "name_first": "Mary",
                "name_last": "Zhu",
                "email": "123@gmail.com",
                "contact_number": "1234567890",
                "address_id": "1"
            })
    print("t3: res = ", res)

def t4():

    res = BaseDataResource.update(
        "users", "user",
            {
                "name_last": "Fu"
            },
            {
                "name_first": "Mary"
            })
    print("t4: res = ", res)

def t5():

    res = BaseDataResource.delete(
        "users", "user", 1)
    print("t5: res = ", res)

#t1()
#t2()
#t3()
#t4()
#t5()