create DATABASE DarwinCell



use DarwinCell



CREATE TABLE Productos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(50) NOT NULL,
    modelo NVARCHAR(50) NOT NULL,
    especificaciones NVARCHAR(255),
    categoria NVARCHAR(20) NOT NULL,
    tipo_accesorio NVARCHAR(20),
    stock INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    imagen VARBINARY(MAX)
);


CREATE TABLE tareas (
    id INT PRIMARY KEY IDENTITY(1,1),
    title NVARCHAR(255),
    description NVARCHAR(255),
    priority NVARCHAR(50),
    status NVARCHAR(50)
);


create table test(
    usr_id int identity (1,1) primary key,
    usr_name NVARCHAR(20),
    usr_password NVARCHAR(15),
    usr_age NVARCHAR(2)
)

create table users(

    usr_id int PRIMARY key IDENTITY(1,1),
    usr_name NVARCHAR(20),
    usr_password NVARCHAR(15),
    usr_privileg NVARCHAR(10)
)


create Table db_admin(
    db_id INT IDENTITY(1,1) PRIMARY KEY,
    db_user NVARCHAR(12),
    db_password  VARCHAR(10)
)


insert into db_admin (db_user, db_password) values ('Miguel', 'AdminDb54' )

select db_password from db_admin

select * from Productos