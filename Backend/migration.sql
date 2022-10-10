CREATE TABLE Users (
  id int,
  email varchar(30) NOT NULL,
  username varchar(30) NOT NULL,
  password varchar(30) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Paddle_court (
  id int,
  max_players int NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Booking (
  id int,
  user_id int NOT NULL,
  paddle_court_id int(30) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id)
      REFERENCES Users (id)
      ON DELETE CASCADE,
  FOREIGN KEY (paddle_court_id)
      REFERENCES Paddle_court (id)
      ON DELETE CASCADE
);

