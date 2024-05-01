CREATE TABLE product (
    pid INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL UNIQUE,
    discount DECIMAL(10,2) DEFAULT 0,
    vendor_price DECIMAL(10,2) NOT NULL,
    selling_price DECIMAL(10,2) NOT NULL,
    CHECK (discount >= 0),
    CHECK (vendor_price >= 0),
    CHECK (selling_price >= 0)
);

CREATE TABLE warehouse (
    wid INT AUTO_INCREMENT PRIMARY KEY,
    warehouse_name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity DECIMAL(10,2) NOT NULL CHECK (capacity > 0),
    manager VARCHAR(255),
    contact VARCHAR(20) UNIQUE,
    CONSTRAINT location_unique UNIQUE (location)
);

CREATE TABLE stock (
    stockid INT AUTO_INCREMENT PRIMARY KEY,
    available_units INT CHECK (available_units > 0),
    pid INT NOT NULL,
    wid INT NOT NULL,
    FOREIGN KEY (pid) REFERENCES product(pid),
    FOREIGN KEY (wid) REFERENCES warehouse(wid)
);

CREATE TABLE employee (
    eid INT AUTO_INCREMENT PRIMARY KEY,
    efname VARCHAR(255) NOT NULL,
    elname VARCHAR(255),
    hiredate DATE NOT NULL,
    telephone VARCHAR(10) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    salary DECIMAL(10,2) NOT NULL CHECK (salary >= 0),
    bonus DECIMAL(10,2) CHECK (bonus > 0)
);

CREATE TABLE customer (
    cid INT AUTO_INCREMENT PRIMARY KEY,
    cfname VARCHAR(255) NOT NULL,
    clname VARCHAR(255),
    telephone VARCHAR(10) NOT NULL UNIQUE,
    address VARCHAR(255) NOT NULL,
    eid INT,
    FOREIGN KEY (eid) REFERENCES employee(eid)
);

CREATE TABLE transporter (
    tid INT AUTO_INCREMENT PRIMARY KEY,
    transporter_company VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255) NOT NULL,
    telephone VARCHAR(10) NOT NULL,
    address VARCHAR(255)
);

CREATE TABLE vendor (
    vid INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    telephone VARCHAR(20) UNIQUE,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE vehicle (
    vno INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(255),
    vehicle_type VARCHAR(255) NOT NULL,
    capacity DECIMAL(10,2) NOT NULL,
    height DECIMAL(10,2) NOT NULL,
    tid INT,
    FOREIGN KEY (tid) REFERENCES transporter(tid)
);

CREATE TABLE orders (
    oid INT AUTO_INCREMENT PRIMARY KEY,
    quantity INT NOT NULL CHECK (quantity > 0),
    order_date DATE NOT NULL,
    required_date DATE NOT NULL,
    shipped_date DATE,
    pid INT,
    cid INT,
    tid INT,
    FOREIGN KEY (pid) REFERENCES product(pid),
    FOREIGN KEY (cid) REFERENCES customer(cid),
    FOREIGN KEY (tid) REFERENCES transporter(tid),
    FOREIGN KEY (vid) REFERENCES vendor(vid),
    FOREIGN KEY (wid) REFERENCES warehouse(wid)
);
CREATE TABLE sale (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    sid INT NOT NULL,
    cid INT NOT NULL,
    sale_date DATETIME NOT NULL,
    quantity_sold INT NOT NULL CHECK (quantity_sold > 0),
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price >= 0),
    total_price DECIMAL(10, 2) NOT NULL CHECK (total_price >= 0),
    FOREIGN KEY (sid) REFERENCES stock(sid),
    FOREIGN KEY (cid) REFERENCES customer(cid)
);



