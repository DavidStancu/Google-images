TEMA INFORMATICA APLICATA 1
312CA Stancu David-ioan

USER-pebble
PASS-pebble123

Pentru aceasta tema am avut de proiectat o galerie de imagini, similara cu 
Google images. Deoarece am avut alegere libera cand vine vorba de tematica, eu 
am ales ca galeria mea sa ia forma unui mini-site de adoptie de pet-rocks :) . 
Urmatoarele cateva paragrafe de mai jos vorbesc despre ce fac fisierele din 
programul principal, precum si despre fisierele html folosite.

base.html - "capul listei", are pe ea toate butoanele de login, upload, gallery 
si about me. 

login.html - Pagina care apare prima si care nu te va lasa sa accesezi altceva 
fara sa te loghezi. Odata ce introduci informatiile necesare, vei primi toate 
permisiunile pe care userul le are (asta include vizionarea galeriei, 
adaugarea/stergerea de imagini etc.). Odata ce esti logat, poti apasa pe acelasi 
buton pentru a te deloga.

home.html - Aici este prezentata galeria, care afiseaza diverse poze ale unor 
pietre adoptate deja(sau in curs de adoptie!). Desi exista mai multe categorii, 
se pot crea altele noi cand se incarca o noua imagine. Imaginile generate vin cu 
un buton de delete, care le va sterge din galerie. Inainte ca imaginile sa poata 
fi sterse, se va intreba inca o data utilizatorul daca este sigur de propria 
decizie. Desi in cerinta scria despre butonul de view, eu am implementat imagina 
sa fie apasabila, pentru a o vedea in full. Astfel nu mai este nevoie de buton. 

upload.html - Fisierul acesta genereaza pagina de upload, care va prezenta un 
form de upload. In acesta va trebui sa introduci imaginea, sa scrii numele 
pietrei, si sa scrii categoria. Cum am spus la home.html, desi sunt doar doua 
categorii momentan, asta nu inseamna ca nu se pot face mai multe. Functia de 
upload accepta doar anumite tipuri de fisiere.

about.html - Introduc cititorul in povestea vietii veterinarului care a creat 
acest centru de adoptie si de ce. Nimic impresionant din punct de vedere f
unctional, ada ca a fost lasat accesibil si pentru persoana nelogata pe site.

logout.html - Inlocuieste Login dupa ce te loghezi. Apasandu-l va trebui sa te 
loghezi din nou pentru a accesa site-ul

Functii:
image - In momentul cand dam upload la o imagine, uploadam aceasta imagine in f
olderul de poze.

thumbnail - Aceasta functie creaza un thumbnail 200x200(px) pe care il afiseaza 
pentru fiecare poza pusa in galerie. Thumbnailul acesta serveste in acelasi timp 
si ca masca pentru linkul catre imaginea full.

delete_image - Va lua pathul de la imaginea care trebuie stearsa, precum si 
pathul thumbnailului, mai apoi stergandu-le.

error404 - Vfisare standard de erori, in cazul in care nu se gaseste pagina 
ceruta. Ma indoiesc ca o sa fie cazul sa fie folosit acum, dar este prezent in 
orice caz.
 