db.createUser(
    {
        user: "uic",
        pwd: "413413413",
        roles: [
            {
                role: "readWrite",
                db: "stock"
            }
        ]
    }
);