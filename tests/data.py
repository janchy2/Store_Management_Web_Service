# AUTHENTICATION DATA
users = {
    # courier
    False : {
        "forename": "John",
        "surname":  "Doe",
        "email":    "john@gmail.com",
        "password": "aA123456",
    },
    # customer
    True: {
        "forename": "Jane",
        "surname":  "Doe",
        "email":    "jane@gmail.com",
        "password": "aA123456",
    },
}

is_registered = {
    False: False,
    True:  False
}


def get_user ( is_customer ):
    global users
    return users[is_customer]


def get_is_user_registered ( is_customer ):
    global is_registered
    return is_registered[is_customer]


def set_is_user_registered ( is_customer, value ):
    global is_registered
    is_registered[is_customer] = value


# LEVEL 0 DATA
get_csv_error0 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,41.44",
    "Category1|Category2,Product2",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])

get_csv_error1 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,x",
    "Category1|Category2,Product2,29.89",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])

get_csv_error2 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,-1.2",
    "Category1|Category2,Product2,29.89",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])


get_data0 = lambda: "\n".join ([
    "Category0,Product0,27.34",
    "Category0,Product1,41.44",
    "Category1|Category2,Product2,29.89",
    "Category2,Product3,37.36",
    "Category6,Product4,13.64",
    "Category3,Product5,26.33",
    "Category5,Product6,20.09",
    "Category4,Product7,47.75",
    "Category4,Product8,15.47",
    "Category0,Product9,41.3",
    "Category0|Category1|Category2,Product10,17.98",
])

get_search_result0 = lambda: {
    "categories": [
        "Category0",
        "Category2",
        "Category1",
        "Category6",
        "Category3",
        "Category5",
        "Category4"
    ],
    "products"  : [
        {
            "categories": [
                "Category0"
            ],
            "id":    1,
            "name":  "Product0",
            "price": 27.34
        },
        {
            "categories": [
                "Category0"
            ],
            "id":    2,
            "name":  "Product1",
            "price": 41.44
        },
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id":    3,
            "name":  "Product2",
            "price": 29.89
        },
        {
            "categories": [
                "Category2"
            ],
            "id":    4,
            "name":  "Product3",
            "price": 37.36
        },
        {
            "categories": [
                "Category6"
            ],
            "id":    5,
            "name":  "Product4",
            "price": 13.64
        },
        {
            "categories": [
                "Category3"
            ],
            "id":    6,
            "name":  "Product5",
            "price": 26.33
        },
        {
            "categories": [
                "Category5"
            ],
            "id":    7,
            "name":  "Product6",
            "price": 20.09
        },
        {
            "categories": [
                "Category4"
            ],
            "id":    8,
            "name":  "Product7",
            "price": 47.75
        },
        {
            "categories": [
                "Category4"
            ],
            "id":    9,
            "name":  "Product8",
            "price": 15.47
        },
        {
            "categories": [
                "Category0"
            ],
            "id":    10,
            "name":  "Product9",
            "price": 41.3
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id":    11,
            "name":  "Product10",
            "price": 17.98
        }
    ]
}

get_csv_error3 = lambda: "\n".join ([
    "Category1,Product0,17.34",
    "Category1,Product1,51.44"
])

get_search_parameters1 = lambda: "name=0"
get_search_result1 = lambda: {
    "categories": [
        "Category0",
        "Category2",
        "Category1"
    ],
    "products"  : [
        {
            "categories": [
                "Category0"
            ],
            "id":    1,
            "name":  "Product0",
            "price": 27.34
        },
        {
            "categories": [
                "Category0",
                "Category1",
                "Category2"
            ],
            "id":    11,
            "name":  "Product10",
            "price": 17.98
        }
    ]
}

get_search_parameters2 = lambda: "name=2"
get_search_result2 = lambda: {
    "categories": [
        "Category2",
        "Category1"
    ],
    "products"  : [
        {
            "categories": [
                "Category1",
                "Category2"
            ],
            "id":    3,
            "name":  "Product2",
            "price": 29.89
        }
    ]
}

get_search_parameters3 = lambda: "category=5"
get_search_result3 = lambda: {
    "categories": [
        "Category5"
    ],
    "products"  : [
        {
            "categories": [
                "Category5"
            ],
            "id":    7,
            "name":  "Product6",
            "price": 20.09
        }
    ]
}

get_search_parameters4 = lambda: "category=5,name=0"
get_search_result4 = lambda: {
    "categories": [],
    "products"  : []
}

# LEVEL 1 DATA
get_order_error0 = lambda: {
    "requests": [
        { }
    ]
}

get_order_error1 = lambda: {
    "requests": [
        {
            "id":       1,
            "quantity": 1
        },
        {
            "id": 1
        }
    ]
}

get_order_error2 = lambda: {
    "requests": [
        {
            "id":       "x",
            "quantity": 1
        }
    ]
}

get_order_error3 = lambda : {
    "requests": [
        {
            "id":       -1,
            "quantity": 1
        }
    ]
}

get_order_error4 = lambda : {
    "requests": [
        {
            "id":       1,
            "quantity": "x"
        }
    ]
}

get_order_error5 = lambda : {
    "requests": [
        {
            "id":        1,
            "quantity": -1
        }
    ]
}

get_order_error6 = lambda : {
    "requests": [
        {
            "id":       10000000000,
            "quantity": 1
        }
    ]
}

get_order_error7 = lambda : {
    "requests": [
        {
            "id":       1,
            "quantity": 1
        }
    ]
}

get_order0 = lambda : {
    "requests": [
        {
            "id":       "Product0",
            "quantity": 2
        },
        {
            "id":       "Product1",
            "quantity": 3
        }
    ]
}

get_order_status0 = lambda: {
    "orders": [
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "CREATED",
            "timestamp": "2023-06-22 20:32:17"
        }
    ]
}

get_order1 = lambda: {
    "requests": [
        {
            "id":       "Product0",
            "quantity": 2
        },
        {
            "id":       "Product1",
            "quantity": 8
        }
    ]
}

get_order_status1 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "CREATED",
            "timestamp": "2023-06-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "CREATED",
            "timestamp": "2022-05-22 21:41:48"
        }
    ]
}

# LEVEL 2 DATA
get_orders_to_deliver_result0 = lambda: {
    "orders": [
        {
            "id":    1,
            "email": "jane@gmail.com"
        },
        {
            "id":    1,
            "email": "jane@gmail.com"
        }
    ]
}


get_order_to_pickup_error0 = lambda: { }

get_order_to_pickup_error1 = lambda: { 
    "id": -1
}

get_order_to_pickup_error2 = lambda: { 
    "id": "x"
}

get_order_to_pickup_error3 = lambda: { 
    "id": 10000000000
}

get_order_to_pickup_error4 = lambda: { 
    "id": 1
}

get_orders_to_deliver_result1 = lambda: {
    "orders": [
        {
            "id":    1,
            "email": "jane@gmail.com"
        }
    ]
}

get_order_status2 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "PENDING",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "CREATED",
            "timestamp": "2022-05-22 21:41:48"
        }
    ]
}

get_pay_error0 = lambda: { }

get_pay_error1 = lambda: { 
    "id": -1
}

get_pay_error2 = lambda: { 
    "id": "x"
}

get_pay_error3 = lambda: { 
    "id": 10000000000
}

get_pay_error4 = lambda: { 
    "id": 1
}

get_delivered_error0 = lambda: { }

get_delivered_error1 = lambda: { 
    "id": -1
}

get_delivered_error2 = lambda: { 
    "id": "x"
}

get_delivered_error3 = lambda: { 
    "id": 10000000000
}

get_delivered_error4 = lambda: { 
    "id": 1
}

get_order_status3 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "CREATED",
            "timestamp": "2022-05-22 21:41:48"
        }
    ]
}

# LEVEL 3 DATA
get_product_statistics0 = lambda : {
    "statistics": [
        {
            "name":    "Product0",
            "sold":    2,
            "waiting": 2
        },
        {
            "name":    "Product1",
            "sold":    3,
            "waiting": 8
        }
    ]
}

get_category_statistics0 = lambda : {
    "statistics": [
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4",
        "Category5",
        "Category6"
    ]
}

get_product_statistics1 = lambda : {
    "statistics": [
        {
            "name":    "Product0",
            "sold":    4,
            "waiting": 0 
        },
        {
            "name":    "Product1",
            "sold":    11, 
            "waiting": 0
        }
    ]
}

get_category_statistics1 = lambda : {
    "statistics": [
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4",
        "Category5",
        "Category6"
    ]
}

get_order2 = lambda: {
    "requests": [
        {
            "id":       "Product4",
            "quantity": 22
        },
        {
            "id":       "Product6",
            "quantity": 22
        }
    ]
}

get_product_statistics2 = lambda :{
    "statistics": [
        {
            "name":    "Product0",
            "sold":    4,
            "waiting": 0
        },
        {
            "name":    "Product1",
            "sold":    11,
            "waiting": 0
        },
        {
            "name":    "Product4",
            "sold":    0,
            "waiting": 22 
        },
        {
            "name":    "Product6",
            "sold":    0,
            "waiting": 22
        }    
    ]
}

get_category_statistics2 = lambda : {
    "statistics": [
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4",
        "Category5",
        "Category6"
    ]
}

get_order_status4 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category6",
                    ],
                    "name":     "Product4",
                    "price":    13.64,
                    "quantity": 22
                },
                {
                    "categories": [
                        "Category5"
                    ],
                    "name":     "Product6",
                    "price":    20.09,
                    "quantity": 22
                }
            ],
            "price":     742.06,
            "status":    "CREATED",
            "timestamp": "2022-05-22 20:32:17"
        },
    ]
}

get_product_statistics3 = lambda :{
    "statistics": [
        {
            "name":    "Product0",
            "sold":    4,
            "waiting": 0
        },
        {
            "name":    "Product1",
            "sold":    11,
            "waiting": 0
        },
        {
            "name":    "Product4",
            "sold":    22,
            "waiting": 0 
        },
        {
            "name":    "Product6",
            "sold":    22,
            "waiting": 0
        }    
    ]
}

get_category_statistics3 = lambda : {
    "statistics": [
        "Category5",
        "Category6",
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4"
    ]
}

get_order_status5 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category6",
                    ],
                    "name":     "Product4",
                    "price":    13.64,
                    "quantity": 22
                },
                {
                    "categories": [
                        "Category5"
                    ],
                    "name":     "Product6",
                    "price":    20.09,
                    "quantity": 22
                }
            ],
            "price":     742.06,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
    ]
}


get_order3 = lambda: {
    "requests": [
        {
            "id":       "Product5",
            "quantity": 30
        }    
    ]
}

get_product_statistics4 = lambda :{
    "statistics": [
        {
            "name":    "Product0",
            "sold":    4,
            "waiting": 0
        },
        {
            "name":    "Product1",
            "sold":    11,
            "waiting": 0
        },
        {
            "name":    "Product4",
            "sold":    22,
            "waiting": 0 
        },
        {
            "name":    "Product6",
            "sold":    22,
            "waiting": 0
        },
        {
            "name":    "Product5",
            "sold":    0,
            "waiting": 30
        }    
    ]
}

get_category_statistics4 = lambda : {
    "statistics": [
        "Category5",
        "Category6",
        "Category0",
        "Category1",
        "Category2",
        "Category3",
        "Category4"
    ]
}

get_order_status6 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category6",
                    ],
                    "name":     "Product4",
                    "price":    13.64,
                    "quantity": 22
                },
                {
                    "categories": [
                        "Category5"
                    ],
                    "name":     "Product6",
                    "price":    20.09,
                    "quantity": 22
                }
            ],
            "price":     742.06,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category3",
                    ],
                    "name":     "Product5",
                    "price":    26.33,
                    "quantity": 30
                }
            ],
            "price":     789.9,
            "status":    "CREATED",
            "timestamp": "2022-05-22 20:32:17"
        },
    ]
}

get_product_statistics5 = lambda :{
    "statistics": [
        {
            "name":    "Product0",
            "sold":    4,
            "waiting": 0
        },
        {
            "name":    "Product1",
            "sold":    11,
            "waiting": 0
        },
        {
            "name":    "Product4",
            "sold":    22,
            "waiting": 0 
        },
        {
            "name":    "Product6",
            "sold":    22,
            "waiting": 0
        },
        {
            "name":    "Product5",
            "sold":    30,
            "waiting": 0
        }    
    ]
}

get_category_statistics5 = lambda : {
    "statistics": [
        "Category3",
        "Category5",
        "Category6",
        "Category0",
        "Category1",
        "Category2",
        "Category4"
    ]
}

get_order_status7 = lambda: {
    "orders": [
        {
            "products" : [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 3
                }
            ],
            "price":     179.0,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products": [
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product0",
                    "price":    27.34,
                    "quantity": 2
                },
                {
                    "categories": [
                        "Category0"
                    ],
                    "name":     "Product1",
                    "price":    41.44,
                    "quantity": 8
                }
            ],
            "price":     386.2,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 21:41:48"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category6",
                    ],
                    "name":     "Product4",
                    "price":    13.64,
                    "quantity": 22
                },
                {
                    "categories": [
                        "Category5"
                    ],
                    "name":     "Product6",
                    "price":    20.09,
                    "quantity": 22
                }
            ],
            "price":     742.06,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
        {
            "products" : [
                {
                    "categories": [
                        "Category3",
                    ],
                    "name":     "Product5",
                    "price":    26.33,
                    "quantity": 30
                }
            ],
            "price":     789.9,
            "status":    "COMPLETE",
            "timestamp": "2022-05-22 20:32:17"
        },
    ]
}