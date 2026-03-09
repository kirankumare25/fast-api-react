-- Create the table structure
CREATE TABLE customers (
    id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    job_title VARCHAR(100),
    gender VARCHAR(20),
    ip_address VARCHAR(45)
);

-- Insert the data
INSERT INTO customers (id, first_name, last_name, email, job_title, gender, ip_address) VALUES
(1, 'Babita', 'Vennart', 'bvennart0@sakura.ne.jp', 'Clinical Specialist', 'Female', '112.60.73.147'),
(2, 'Rivi', 'Stent', 'rstent1@businessinsider.com', 'Sales Representative', 'Female', '163.98.82.155'),
(3, 'Anica', 'Leeman', 'aleeman2@hexun.com', 'Technical Writer', 'Female', '137.237.238.222'),
(4, 'Correy', 'Petrina', 'cpetrina3@reddit.com', 'Graphic Designer', 'Female', '110.17.42.191'),
(5, 'Euphemia', 'Gee', 'egee4@google.co.uk', 'Recruiter', 'Female', '144.146.49.50'),
(6, 'Gianni', 'Dunmore', 'gdunmore5@noaa.gov', 'Junior Executive', 'Male', '46.144.137.56'),
(7, 'Candi', 'Bernardon', 'cbernardon6@washington.edu', 'Marketing Assistant', 'Female', '37.124.22.141'),
(8, 'Donna', 'MacShirrie', 'dmacshirrie7@baidu.com', 'Sales Representative', 'Female', '58.90.4.167'),
(10, 'Edee', 'Aurelius', 'eaurelius9@ft.com', 'Senior Editor', 'Non-binary', '124.203.135.89'),
(9, 'Magdalene', 'Evans', 'mevans8@cdc.gov', 'Environmental Specialist', 'Female', '227.122.126.133');