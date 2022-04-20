#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Created By  : Emil Bystrup Lenschau, Jonas Hvid Nielsen, Magnus Christophersen, Maria Buur and Mathias Villa Fonseca
# Created Date: 05/11/2022
# version ='1.0'
# ---------------------------------------------------------------------------
""" Dette script har til formål at præsentere sammenkoblingen mellem database og python.
Dette script viser hvordan ladeoperatøren Clever kan vise deres kunder, hvor lang tid de skal bruge på at lade deres bil,
dette gøres for at skabe et incitament til at rykke deres biler, når deres opladning er færdig. Hvis ikke de rykker deres
bil, vil de blive præsenteret for et gebyr, der vil stige i pris i takt med tiden som ladningen er overskredet.  """
# ---------------------------------------------------------------------------
from Repository import Repository               #Repository er et tilknyttet script, som forbinder Python med Database.
import math                                     #math bruges til at afrunde tal.
import pandas as pd

class Intro():

    def greeting(self):

        print("\nHej, velkommen til Clever\n")
        print("Indtast venligst dine login oplysninger\n")

intro = Intro()
intro.greeting()

class Login():                                          #Definerer en class som indeholer en række funktioner.

    def __init__(self):                                 #Definerer opstarts funktionen. Denne funktion kører når Login() kører.

        self.brugernavn = input('E-mail : ')             #Definerer brugernavn som et input fra bruger
        self.adgangskode = input('Adgangskode : ')      #Definerer adgangskode som et input fra bruger

    def login_check(self):                              #login_check funktion. " By using the “self” keyword we can access the attributes and methods of the class in python. It binds the attributes with the given arguments. " (https://www.geeksforgeeks.org/self-in-python-class/)

        file = open("Login.txt","r")                    #Åbner Login.txt fil i read mode "r". Der kan kun læses i filen i dette mode.

        if '@' not in self.brugernavn:                  #If statement. Hvis @ ikke er en del af brugernavnet gør dette:
            print('E-mail skal indeholde @')
            print('Log venligst ind igen')
            login = Login()                             #Kører Login() class på ny
            login.login_check()                         #Kører login_check class efter __init__ class.

        elif self.brugernavn and self.adgangskode in file:      #Elif statement. Elif bruges, da der er flere "if". Hvis brugernavn og adgangskode er i fil gør dette:
            print('\nVelkommen', self.brugernavn)

        else:                                                   #else statement. Hvis brugernavn og adgangskode ikke er i fil gør dette:
            question = input("\nE-mail eller Adgangskode er forkert. \nHar du godkendt dine login oplysninger? ja/nej : ")

            if question == 'ja':                                #if statement. Hvis input = "ja" gør dette:
                print('Prøv venligst at logge ind igen')
                login = Login()                                 #Kører Login() class på ny
                login.login_check()                             #Kører login_check class efter __init__ class.

            elif question == "nej":                             #elif statement. Hvis input = "nej" gør dette:
                print('Du skal skrive din E-mail og adgangskode første gang du logger ind.')
                print('Dette skal du gøre for at godkende dine oplysingner i vores system.')
                self.approve_login()                            #Kører funktionen approve_login()

            else:                                               #else start på ny.
                login = Login()
                login.login_check()

    def approve_login(self):                                                            #approve_login funktion. Godkender login.

        file = open("Login.txt", "a")                                                   #Åbner .txt fil i append mode "a". I dette mode er det kun muligt at tilføje noget til filen.

        file.write("\n" + input('E-mail : '))                                      #.write gør at man kan skrive noget der bliver tilføjet til filen. Her er det brugerens input der bliver tilføjet.
        file.write("\n" + input('Adgangskode : '))
        print("Login godkendes")
        print('Login er godkendt i vores system. Prøv venligst at logge ind igen.')

        file.close()                                                                    #Lukker filen Login.txt der er blevet navngivet "file" i 46.

        login = Login()                                                                 #Starter på ny.
        login.login_check()

login = Login()                     #Kører Login() class og dermed __init__
login.login_check()                 #Kører login_check class efter __init__ class.

class Car():                                                         #I denne class er det muligt at vælge en bil fra en liste importeret fra en database.

    def __init__(self):

        print("Vælg venligst din bil fra nedenstående liste.\n")
        re = Repository()
        re.SetConnection()                                          #Connect til database
        self.List_Of_Cars = re.GetAllTolist("cleverapp.evstats")    #Hent en liste over biler fra databasen cleverapp og tabel evstats.
        for i in self.List_Of_Cars:                                 #For loop der gør fremvisningen af data pænere ved at placere hvert row fra databasen på en linje.
            print(i)

    def choose_car(self):

        self.Choice_of_car = input("\nVælg venligst din bil ved at skrive det fulde navn for eksempel (Audi e-tron 50)\n")
        for x, y in self.List_Of_Cars:                                                                                          # x og y hentyder til bilmærke og batterikapacitet. Vi specificere at det skal være x værdien og dermed bilmærket.
            if x in self.Choice_of_car:                                                                                         #Hvis bilmærket er i databasen, print bil valgt.
                print("Bil valgt", "'", x, "'\n")
                self.Capacity = y                                                                                               #y værdien bruges til at beregne ladetid i menupunkt 3.
                                                                                                                                #Her ville vi have haft et elif/else statement, men det blev ikke tilladt af python.





car = Car()
car.choose_car()

class Charging_Type():                                                                                                          # En class der har til mål at få brugerinput omkring ladetyper.

    def __init__(self):                                                                                                         #En query der har til formål at fremskaffe data om ladetyper
        print("Vælg venligst, hvilke / hvilken ladetype din bil accepterer.")
        re = Repository()
        re.SetConnection()
        self.List_Of_Charging_Types = re.GetDistinctTolist("ConnectorVariantName", "cleverapp.charging_types")                  #Vi specificere hvilken kollonne fra databasen vi distinct vil have og fra hvilken tabel.
        for i in self.List_Of_Charging_Types:
            print(i)

    def choose_charging_type(self):                                                                                             #Valg opstillet efter ja / nej pricip.
                                                                                                                                #Hvis brugeren skriver j bliver værdien j gemt for den enkelte type.
        self.IEC_Type_1 = input("\nAccepterer din bil IEC Type 1? ----- j eller n\n")                                           #På denne måde kan vi huske, hvilke ladetyper brugeren har til senere brug.
        if self.IEC_Type_1 == "j":
            print(self.List_Of_Charging_Types[0], "valgt")
        elif self.IEC_Type_1 == "n":
            print(self.List_Of_Charging_Types[0], "fravalgt")
        else:
            ct.choose_charging_type()

        self.IEC_Type_2 = input("\nAccepterer din bil IEC Type 2? ----- j eller n\n")
        if self.IEC_Type_2 == "j":
            print(self.List_Of_Charging_Types[1], "valgt")
        elif self.IEC_Type_2 == "n":
            print(self.List_Of_Charging_Types[1], "fravalgt")
        else:
            ct.choose_charging_type()

        self.CCS = input("\nAccepterer din bil CCS? ----- j eller n\n")
        if self.CCS == "j":
            print(self.List_Of_Charging_Types[2], "valgt")
        elif self.CCS == "n":
            print(self.List_Of_Charging_Types[2], "fravalgt")
        else:
            ct.choose_charging_type()

        self.CHAdeMO = input("\nAccepterer din bil CHAdeMO? ----- j eller n\n")
        if self.CHAdeMO == "j":
            print(self.List_Of_Charging_Types[3], "valgt")
        elif self.CHAdeMO == "n":
            print(self.List_Of_Charging_Types[3], "fravalgt")
        else:
            ct.choose_charging_type()



ct = Charging_Type()
ct.choose_charging_type()

class Menu():                       #Definerer Menu() som en class

    #Menu der viser valgmuligheder
    def __init__(self):
        print("----------------------------------------------------------------------------------")
        print("MENU")
        print("1. Se et overblik over ladepunkter")
        print("2. Se liste over gebyrer")
        print("3. Se din forventede ladetid")
        print("4. Afslut")
        print("----------------------------------------------------------------------------------")

    #Funktion hvor der vælges hvilket menupunkt man ønsker at tilgå. Består af "if", "elif" og "else" statements.
    def choice(self):

        choice = input("\n" + "Venligst vælg hvilket menupunkt du ønsker at tilgå." + "\n" + "Du vælger menupunkt ved at taste det nummer der står ud for det menupunkt du ønsker at vælge. (1, 2, 3, 4, 5, 6)" + "\n")

        if choice == "1":

            overview()


        elif choice == "2":

            print("Her kan du se hvad du skal betale per kvarter du overskrider din ladetid")
            print("('Kr', Minutter)")

            fee()

        elif choice == "3":

            Expected_Charging_Time().Menu2()
            Expected_Charging_Time().Choose_charge()


        elif choice == "4":                             #Afslutter programmet

            exit()
        else:
            self.choice()                               #Hvis nummeret der indtastes ikke stemmer overens med nummeret i menuen, sendes brugeren tilbage til valg af menupunkt(choice(self)).

    def return_or_leave(self):

        print("----------------------------------------------------------------------------------")
        print("1. Gå tilbage til menu")
        print("2. Afslut")
        print("----------------------------------------------------------------------------------")

        return_or_leave = input("Vælg venligst ved at taste 1 eller 2\n")

        if return_or_leave == "1":
            menu = Menu()           #Kører Menu class på ny med __init__ først
            menu.choice()           #Kører choice() funktion efter __init__ funktion.

        elif return_or_leave == "2":
            exit()                  #Afslutter programmet/script

        else:
            self.return_or_leave()  #Kører return_or_leave funktion på ny.


class overview():                   #Denne class giver et overblik er ladepunkter, som brugeren kan benytte med sin / sine ladetyper.

    def __init__(self):

        PostalCode = input("Skriv venligst dit postnummer og få et overblik over ladepunkter i din by.\n")
        print("\nHer ses et overblik over alle ladepunkter, hvor din bil kan lade.\n")
        print("('LOKATION', 'VEJNAVN', 'VEJNUMMER', 'POSTNUMMER', 'BY', 'LADETYPE', 'EFFEKT')")

        if ct.IEC_Type_1 == "j":                                                                                #Hvis brugeren har trykket ja til at have IEC Type 1 vil resultater fra databasen med type 1 vises her
            re = Repository()
            re.SetConnection()
            self.List_Of_Charging_Points = re.OverviewOfChargingPointsTolist("'%IEC Type 1%'", PostalCode)      #Connect til database og kører query.
            for i in self.List_Of_Charging_Points:
                print(i)

        if ct.IEC_Type_2 == "j":
            re = Repository()
            re.SetConnection()
            self.List_Of_Charging_Points = re.OverviewOfChargingPointsTolist("'%IEC Type 2%'", PostalCode)
            for i in self.List_Of_Charging_Points:
                print(i)

        if ct.CCS == "j":
            re = Repository()
            re.SetConnection()
            self.List_Of_Charging_Points = re.OverviewOfChargingPointsTolist("'%CCS%'", PostalCode)
            for i in self.List_Of_Charging_Points:
                print(i)

        if ct.CHAdeMO == "j":
            re = Repository()
            re.SetConnection()
            self.List_Of_Charging_Points = re.OverviewOfChargingPointsTolist("'%CHAdeMO%'", PostalCode)
            for i in self.List_Of_Charging_Points:
                print(i)

        menu.return_or_leave()

class fee():

    def __init__(self):
        re = Repository()
        re.SetConnection()
        self.List_Of_Fees = re.GetTwoTolist("parking_fees", "fee", "Minutes" )
        for i in self.List_Of_Fees:
            print(i)

        menu.return_or_leave()

class Expected_Charging_Time():

    def Menu2(self):                                                                                    #Menu 2 for hurtigere oveblik.
        print("----------------------------------------------------------------------------------")
        print("MENU")
        print("1. Se ladetid med 11 kW")
        print("2. Se ladetid med 22 kW")
        print("3. Se ladetid med 43 kW")
        print("4. Se ladetid med 50 kW")
        print("5. Se ladetid med 150 kW")
        print("6. Afslut")
        print("----------------------------------------------------------------------------------")

    def Choose_charge(self):
        charge_choice = input("\n" + "Venligst vælg hvilket menupunkt du ønsker at tilgå." + "\n" + "Du vælger menupunkt ved at taste det nummer der står ud for det menupunkt du ønsker at vælge. (1, 2, 3, 4, 5, 6)" + "\n")

        if charge_choice == "1":
            Expected_Charging_Time().Charge_Time_11()
        if charge_choice == "2":
            Expected_Charging_Time().Charge_Time_22()
        if charge_choice == "3":
            Expected_Charging_Time().Charge_Time_43()
        if charge_choice == "4":
            Expected_Charging_Time().Charge_Time_50()
        if charge_choice == "5":
            Expected_Charging_Time().Charge_Time_150()
        if charge_choice == "6":
            exit()

    def return_or_leave1(self):

        print("----------------------------------------------------------------------------------")
        print("1. Gå tilbage til menu")
        print("2. Afslut")
        print("----------------------------------------------------------------------------------")

        return_or_leave1 = input("Vælg venligst ved at taste 1 eller 2\n")

        if return_or_leave1 == "1":
            Expected_Charging_Time().Menu2()
            Expected_Charging_Time().Choose_charge()

        elif return_or_leave1 == "2":
            exit()                  #Afslutter programmet/script

        else:
            self.return_or_leave1()  #Kører return_or_leave funktion på ny.

    def Charge_Time_11(self):
        print("Med en 11 kW lader vil din bil oplades fra 0-100 procent på cirka\n")                                                        #Viser hvor hurtigt den valgte bil kan lades op ved en effekt på 11 KW.
        print(round((car.Capacity / 11)*60), "Minutter\nEller")
        print(math.floor(car.Capacity / 11), "Timer og ", round(((car.Capacity / 11) - (math.floor(car.Capacity / 11)))*60), "Minutter")   #Viser timer rundet ned til nærmeste time. Derefter timer ialt minus den der er rundet ned for at få antal manglende timer der kan omregnes til klokkeformat. Dernæst gange 60 for at få minutter,
        Expected_Charging_Time().return_or_leave1()

    def Charge_Time_22(self):
        print("Med en 22 kW lader vil din bil oplades fra 0-100 procent på cirka\n")
        print(round((car.Capacity / 22)*60), "Minutter\nEller")
        print(math.floor(car.Capacity / 22), "Timer og ", round(((car.Capacity / 22) - (math.floor(car.Capacity / 22)))*60), "Minutter")
        Expected_Charging_Time().return_or_leave1()

    def Charge_Time_43(self):
        print("Med en 43 kWh lader vil din bil oplades fra 0-100 procent på cirka\n")
        print(round((car.Capacity / 43)*60), "Minutter\nEller")
        print(math.floor(car.Capacity / 43), "Timer og ", round(((car.Capacity / 43) - (math.floor(car.Capacity / 43)))*60), "Minutter")
        Expected_Charging_Time().return_or_leave1()

    def Charge_Time_50(self):
        print("Med en 50 kWh lader vil din bil oplades fra 0-100 procent på cirka\n")
        print(round((car.Capacity / 50)*60), "Minutter\nEller")
        print(math.floor(car.Capacity / 50), "Timer og ", round(((car.Capacity / 50) - (math.floor(car.Capacity / 50)))*60), "Minutter")
        Expected_Charging_Time().return_or_leave1()

    def Charge_Time_150(self):
        print("Med en 150 kWh lader vil din bil oplades fra 0-100 procent på cirka\n")
        print(round((car.Capacity / 150)*60), "Minutter\nEller")
        print(math.floor(car.Capacity / 150), "Timer og ", round(((car.Capacity / 150) - (math.floor(car.Capacity / 150)))*60), "Minutter")
        Expected_Charging_Time().return_or_leave1()



# '22'
# 'DC - 50 kW'
# 'AC - 22 kW'
# 'AC - 43 kW'
# '50'
# '11'
# '150'
# '43'

menu = Menu()
menu.choice()
