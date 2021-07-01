-- show databases;
use trafficManagementSystem;

drop table if exists logIN;
drop table if exists callHospital;
drop table if exists informPetrolPump;
drop table if exists deliveryBoy;
drop table if exists ambulance;
drop table if exists vehicle;
drop table if exists petrolPump;
drop table if exists trafficPolice;
drop table if exists hospital;
drop table if exists citizen;
drop table if exists location;

create table logIN(
ID int not null, role int not null, password varchar(20) not null,
primary key(ID, role)
);

create table location(
X int not null, Y int not null,
primary key(X, Y), cost int not null default 0
);

create table citizen(
ID int not null, name varchar(100) not null, wallet int not null, contact int not null, fuel int not null, X int not null, Y int not null, status int not null default 0, path varchar(100),
primary key(ID), 
foreign key (X,Y) references location(X,Y)
);


create table hospital(
ID int not null, contact int not null, availBed int not null, X int not null, Y int not null,
primary key(ID), 
foreign key (X,Y) references location(X,Y)
);


create table trafficPolice(
ID int not null, name varchar(100) not null, wallet int not null, contact int not null, X int not null, Y int not null,
primary key(ID),
foreign key (X,Y) references location(X,Y)
);


create table petrolPump(
ID int not null, contact int not null, X int not null, Y int not null,
primary key(ID), 
foreign key (X,Y) references location(X,Y)
);


create table deliveryBoy(
ID int not null, pumpID int not null,
primary key(ID), 
foreign key (pumpID) references petrolPump(ID), foreign key (ID) references citizen(ID)
);


create table ambulance(
ID int not null, hospitalID int not null,
primary key(ID), 
foreign key (hospitalID) references hospital(ID), foreign key (ID) references citizen(ID)
);

-- All stackholder table complete

-- select * from location, citizen, hospital, ambulance, petrolPump, deliveryBoy, trafficPolice;


create table callHospital(
citizenID int not null, hospitalID int not null, X int not null, Y int not null,
foreign key (X,Y) references citizen(X,Y), foreign key (citizenID) references citizen(ID), foreign key (hospitalID) references hospital(ID), 
primary key(citizenID, X,Y)
);


create table informPetrolpump(
citizenID int not null, pumpID int not null, X int not null, Y int not null,
foreign key (X,Y) references citizen(X,Y), foreign key (citizenID) references citizen(ID), foreign key (pumpID) references petrolPump(ID), 
primary key(citizenID, X,Y)
);


create table vehicle(
registrationNumber int not null, type int not null, document float not null default 0.0, citizenID int not null,
primary key(registrationNumber),foreign key (citizenID) references citizen(ID)
);

-- alter table deliveryBoy add inuse int not null default 0;
-- select * from callHospital;
-- select * from ambulance;
-- select * from petrolPump;
-- select * from citizen;
-- -- select * from location;
-- select * from hospital;
-- truncate table informPetrolpump;
-- update ambulance set inuse = 1 where id = 5;
-- select * from deliveryBoy;
-- select count(pumpID) from deliveryBoy where inuse <> 1 and pumpID = 1;
-- select * from informPetrolpump;
-- select * from logIN;
