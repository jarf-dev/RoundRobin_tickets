CREATE TABLE "RutinasDisponibles" (
	"id"	SERIAL primary key,
	"NombreRutina"	TEXT,
	"DescripcionRutina"	TEXT,
	"idVistaZendesk"	TEXT,
	"NombreVistaZendesk"	TEXT,
	"idAlgoritmo"	INTEGER,
	"esActivado"	INTEGER,
	"ultimoCambioEstado"	TEXT,
	"Etiquetas"	TEXT
	);

CREATE TABLE "CargaAgentes" (
	"id"	serial NOT NULL UNIQUE,
	"idAgenteZendesk"	bigint,
	"idRutina"	INTEGER,
	"esActivado"	INTEGER,
	"ultimoCambioEstado"	TEXT,
	"marcadorTurno"	INTEGER DEFAULT 0,
	"cargaTrabajo"	INTEGER DEFAULT 0,
	FOREIGN KEY("idRutina") REFERENCES "RutinasDisponibles"("id"),
	PRIMARY KEY("id")
);

CREATE TABLE "AlgoritmosDisponibles" (
	id int8 NULL,
	"nombreAlgoritmo" text NULL,
	"descripcionAlgoritmo" text NULL,
	"nombreArchivo" text NULL
);

CREATE VIEW "RutinasDisponiblesTotAgentes" AS
SELECT a.id, a."NombreRutina", a."DescripcionRutina", a."idVistaZendesk",a."NombreVistaZendesk", a."idAlgoritmo", a."esActivado", a."ultimoCambioEstado", b.TotAgentes FROM public."RutinasDisponibles" AS a
LEFT JOIN (SELECT c."idRutina", count(c."idAgenteZendesk") AS TotAgentes FROM public."CargaAgentes" as c GROUP BY c."idRutina") AS b ON a."id"=b."idRutina";