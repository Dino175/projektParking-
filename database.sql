
CREATE TABLE Vozilo (
    RegistarskaOznaka TEXT PRIMARY KEY,
    Marka TEXT NOT NULL,
    Model TEXT NOT NULL,
    Boja TEXT,
    GodinaProizvodnje INTEGER
);


CREATE TABLE ParkirnoMjesto (
    IdentifikatorMjesta TEXT PRIMARY KEY,
    Status TEXT NOT NULL,
    VrijemeParkiranja TEXT
);
