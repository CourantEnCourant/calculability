% autre algorithme de duplication

% duplique un s�rie de b�tons. La s�rie est encadr�e � droite et � gauche par un 0 au moins.
% Si l'oeil est positionn� sur un 0, la s�rie � dupliquer est vide.
% Si l'oeil est positionn� sur un 1, la s�rie � dupliquer est constitu�e de TOUS les b�tons
% � droite et � gauche de la position de l'oeil.

% -- Exemples de ruban d'entr�e

   %  00111110000000  ou bien   00111110000000
   %    X                            X

% -- Dans ces deux exemples, la s�rie � dupliquer est constitut�e de 5 b�tons.

% Dans le ruban de sortie, la s�rie initiale est s�par�e par un 0 de son double et l'oeil 
% est positionn� sur le b�ton le plus � gauche du double.
% -- Ruban de sortie des exemples pr�c�dents :

   %  00111110111110  
   %          X                            


si (0) fin} % arr�t imm�diat si l'oeil est positionn� sur un 0 (la s�rie � dupliquer est vide)

% d�place l'oeil jusqu'au 0 � l'extr�mit� droite de la s�rie de b�tons
boucle 
  D 
  si (0) fin } 
}  
% puis se positionne sur la case imm�diatement � droite
D 


boucle
  1
  boucle G si (0) fin }}
  boucle G si (1) fin }}
  G 
I
  si (0) fin } 
  D
  0
  boucle D si (1) fin }}
  boucle D si (0) fin }}
}

D
boucle D si (1) fin } 1 }
G
0
D
I



#