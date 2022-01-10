create table staging_city_population(
	year varchar(30),
    population varchar(30),
    city varchar(30),
    state varchar(30)
);

create table staging_global_land_temp(
	dt date,
  	averageTemperature float,
  	averageTemperatureUncertainty float,
    city varchar(30),
  	country varchar(30),
  	latitude varchar(10),
  	longitude varchar(10)
);

create table dim_city_pop(
	year int not null,
  	population int not null,
  	city varchar(30) not null,
  	state varchar(30),
  	primary key(city,year)
);

create table dim_land_temp(
	dt date not null,
  	city varchar(30) not null,
  	averageTemperature float not null,
  	averageTemperatureUncertainty float,
  	primary key(city,dt)
);

create table dim_city(
	city varchar(30) not null,
  	country varchar(30),
  	latitude varchar(10),
  	longitude varchar(10),
  	primary key(city)
);

create table dim_time(
	dt date,
  	year int,
  	month int,
  	day int,
  	primary key(dt)
);

create table fact_city_temp_n_pop(
	id varchar(50) not null,
  	year int,
  	city varchar(30),
  	country varchar(30),
  	state varchar(30),
  	population int,
  	averageTemperature float,
  	averageTemperatureUncertainty float,
  	primary key(id)
);
