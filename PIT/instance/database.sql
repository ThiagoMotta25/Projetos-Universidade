SQLite format 3   @                                                                     .j�� � �G�                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            �D�ktablenotenoteCREATE TABLE note (
	id INTEGER NOT NULL, 
	data VARCHAR(10000), 
	date DATETIME, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
)�A�]tablesensorsensorCREATE TABLE sensor (
	id INTEGER NOT NULL, 
	name VARCHAR(80) NOT NULL, 
	unit VARCHAR(20) NOT NULL, 
	value FLOAT NOT NULL, 
	timestamp DATETIME, 
	PRIMARY KEY (id)
)�A�etableuseruserCREATE TABLE user (
	id INTEGER NOT NULL, 
	email VARCHAR(150), 
	password VARCHAR(50), 
	full_name VARCHAR(150), 
	type VARCHAR(50), 
	PRIMARY KEY (id), 
	UNIQUE (email)
)'; indexsqlite_autoindex_user_1user          i 3i�                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      �B !�Qash@ap.comscrypt:32768:8:1$3wr0whKI79kf5TC0$b786d67bd67dcdaa9f6fe8715737153bd69999aab2739a37c91fb323d2e93915906b8f857abe564395a7b4449cfbd01df1fa7a1fb842d0bbe079f9f8dc92c01dAsh Apashclient�G )�Q!joao@tagala.ptscrypt:32768:8:1$K5XRJlz8YZpV5kC5$2eaa2a2e1ef92443a1b9d9eb66159729ac57d82a4a20feb5f7805846fc361c4afeef77c16e4a1bac4f11adc1356bf44fa09155075d908a2315d15a4f074e837eJoao Silvaclient�J -�Q%thiago@gmail.comscrypt:32768:8:1$NviTRwEj08l37Sps$0d463d218343b7be26c87d8708ac7cb4bf3ba5cf65f543dab84ce88e999bec906faadb6e9940dce2a3d549f13ccb1bfe51da0c56431daa4bdb3128f05b7f17f1Thiago Mottaadmin
   � ���                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            !ash@ap.com)joao@tagala.pt-	thiago@gmail.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    �                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         3	ok
2024-05-27 19:33:21