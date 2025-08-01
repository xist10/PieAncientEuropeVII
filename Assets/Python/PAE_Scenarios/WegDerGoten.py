# Scenario Weg der Goten by brettschmitt

# Imports
from CvPythonExtensions import (CyGlobalContext, UnitAITypes,
		CyMap, CyPopupInfo, ButtonPopupTypes, DirectionTypes,
		CyTranslator, CyInterface, ColorTypes, CyCamera, plotXY,
		CyGInterfaceScreen, EventContextTypes, CyGame)
# import CvEventInterface
import CvUtil
# import PyHelpers
# import CvCameraControls
import PAE_Unit
import PAE_City
# for popups with dds:
import CvScreenEnums
import Popup as PyPopup

# Defines
gc = CyGlobalContext()

# Internes für einmalige Events
GotenCities3Pop6 = False
GotenErsteProvinzstadt = False

#[EVENT-1.2] Jagdgebiet wird erweitert:
#8 Plots um eigene Städte kann Nahrung erjagt werden
# => befindet sich in PAE_Unit getHuntingDistance()

def onGameStart():
#[EVENT-1.1] Vor Spielstart, Auswürfeln der Heiligen Städte.
	# Nordische Mythen: Cherusker (50%), Markomanne (25%), Hermundure (25%)
	# Keltische Mythen: Britonen (50%), Gallier (25%) Aquitanier (25%)
	# Die gewürfelte heilige Stadt bekommt ihr Wunder eingebaut: Donareiche bzw. Heiliger Hain
	lPlayerRelNordic = [1,1,3,4]
	lPlayerRelCeltic = [5,5,6,8]

	# Nordic Gods
	iRand = CvUtil.myRandom(len(lPlayerRelNordic), "WDG_RelNordic")
	iPlayer = lPlayerRelNordic[iRand]
	pPlayer = gc.getPlayer(iPlayer)
	lCities = []
	(loopCity, pIter) = pPlayer.firstCity(False)
	while loopCity:
		if not loopCity.isNone() and loopCity.getOwner() == iPlayer:
			lCities.append(loopCity)
		(loopCity, pIter) = pPlayer.nextCity(pIter, False)
	iRand = CvUtil.myRandom(len(lCities), "WDG_CitiesRelNordic")
	pCity = lCities[iRand]
	gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_NORDIC"), pCity, True)
	pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_NORDIC_SHRINE"), 1)

	# Celtic Gods
	iRand = CvUtil.myRandom(len(lPlayerRelCeltic), "WDG_RelCeltic")
	iPlayer = lPlayerRelCeltic[iRand]
	pPlayer = gc.getPlayer(iPlayer)
	lCities = []
	(loopCity, pIter) = pPlayer.firstCity(False)
	while loopCity:
		if not loopCity.isNone() and loopCity.getOwner() == iPlayer:
			lCities.append(loopCity)
		(loopCity, pIter) = pPlayer.nextCity(pIter, False)
	iRand = CvUtil.myRandom(len(lCities), "WDG_CitiesRelCeltic")
	pCity = lCities[iRand]
	gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_CELTIC"), pCity, True)
	pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_CELTIC_SHRINE"), 1)


# [EVENT-2.1] Rom (Player 14) und Byzanz (Player 12) haben ein permanentes Verteidigungsbündnis bis zur Reichsteilung
	#gc.getTeam(gc.getPlayer(14).getTeam()).signDefensivePact(12)



def DawnOfMan():
	# Bild PopUp bei Spielstart
	#Ihr seid Alarich der Gote!
	#Gestern noch ein angesehener Clanfürst im Gotenreich, heute ein Verbannter. Die alte Heimat ist zum Feind geworden, ihr müsst sie als Barbaren betrachten! Aber die Gemeinschaft ist schwach, wir sollten nicht zögern und zurückschlagen! Einer eurer Gefolgsleute ist dortgeblieben, um die Lage für euch auszukundschaften.
	#Wir sollten sofort nach Hagelsberg marschieren. Dem Ältesten persönlich die Tür eintreten, durch die er uns grade erst hinausgeworfen hat. Und dort ist auch der zentrale Rüstungsschneider, von wo aus das ganze Reich versorgt wird.
	#Oder wir beginnen unseren Feldzug weiter südlich die Weichsel rauf, wo mit weniger Widerstand zu rechnen ist. Interessant sind vor allem die Pferde in Gotonen. Die Reiterei ist eine für uns noch recht neue Angelegenheit, könnte aber ein wichtiger Pfeiler der Armee werden.
	#Die Entscheidung trefft Ihr, und das Schicksal der wahren Goten liegt in Eurer Hand.
	#<EROBERT EINE STADT>
	szTextHead = ""
	szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GAME_START", ("", ))
	PopUpDDS("Art/Scenarios/WegDerGoten/WDG01.dds",szTextHead,szTextBody)



def onCityAcquired(iPreviousOwner, iNewOwner, pCity):

	lGerVandalen = [1,2,3,4,9]
	pNewOwner = gc.getPlayer(iNewOwner)
	iNumCities = pNewOwner.getNumCities()
	if iNumCities > 1:
#[EVENT-3.1] Es gibt Siedler: Ab der 2. eroberten Stadt gibt es bei jeder Eroberung eine 10% Chance
		if CvUtil.myRandom(10, "WDG_SettlerOnCityAcquired") == 1:
			pNewOwner.initUnit(gc.getInfoTypeForString("UNIT_SETTLER"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_SETTLE, DirectionTypes.DIRECTION_SOUTH)

			# Kultur setzen
			#iCulture = pCity.getCulture(iPreviousOwner) / 2
			#pCity.setCulture(iPreviousOwner, iCulture, 1)
			#pCity.setCulture(iNewOwner, iCulture, 1)

			#Ihr habt durch eure Eroberungen viele Leute um euch gesammelt, die nach einer Heimat verlangen. Weist ihnen einen Platz zu, an dem sie ihre eigene Siedlung aufbauen sollen. Sie haben genug gekämpft und verdienen einen Ort, den sie ihr zu Hause nennen.
			#<IHR ERHALTET 1 SIEDLER>
			if pNewOwner.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_SETTLER", ("", )))
				popupInfo.addPopup(pNewOwner.getID())

		if iNumCities == 4:
#[EVENT-12.1] Wenn der Spieler 4 Städte hat (inkl. Hauptstadt):
			#Abwarten bis der Aufstand vorbei ist -> DANN
			#In [get.Capitalname] wird ein Thing gesetzt (wenn es noch nicht da ist), und das Thing-Tagungen Event findet statt
			#Das gotische Reich erweitert sich stetig. Wir kontrollieren jetzt vier ehemalige Fürstentümer.
			#Genug, um eine wichtige Rolle bei den Things der Germanenvölker einzunehmen. Eine Rolle, die noch keinem Goten jemals zugestanden wurde. Der Älteste konnte seinerzeit froh sein, wenn er überhaupt eingeladen war.
			#<DAS GROSSE THING FINDET IN [get.Capitalname] STATT> (Gebäude: Thing-Tagungen)
			pCity = pNewOwner.getCapitalCity()
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_THING"), 1)
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_THING_CITY"), 1)
			if pNewOwner.isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_THING", (pCity.getName().upper(), )))
				popupInfo.addPopup(pNewOwner.getID())

#[EVENT-10.3] Wenn der Gote die erste Stadt erobert
	#Der Palast, Monolith und Heldendenkmal wird gesetzt.
	# Die heilige Stadt der Nordischen Mythen wird 1x aufgedeckt
	elif iNewOwner == 0 and iNumCities == 1:
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_PALACE"), 1)
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MONOLITH"), 1)
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MONUMENT"), 1)

		# Die Gotenhauptstadt bekommt 80% Kultur.
		iPreviousCulture = pCity.getCulture(iPreviousOwner) / 10
		pCity.setCulture(iPreviousOwner, iPreviousCulture * 2, 1)
		pCity.setCulture(iNewOwner, iPreviousCulture * 8, 1)

		# Der erste Schritt ist getan. Ihr habt [get.cityname] erobert!
		# Dies wird die Hauptstadt eines neuen, geeinten Gotenreiches sein. Es soll das größte Reich aller Zeiten in Germanien werden, das sich am Ende mit dem der Römer messen kann.
		#Ihr lasst die Leute alle Schäden reparieren und hier unsere Heimat aufbauen. Wir sollten auch bald einen Tempel errichten, um den Göttern zu huldigen. Der Älteste und seine Sippe haben scheinbar geschlafen die letzten Jahre, viele Gebäude sind noch nichtmal geplant.
		#Die heilige Donareiche steht schon seit den Ahnen unter Kontrolle von [get.Leadername], das Zentrum der Götter in [get.cityname] sollten wir irgendwann unter gotische Kontrolle bringen..
		#Das Überraschungsmoment ist jetzt auf unserer Seite. Es empfielt sich, schnell weiter zu ziehen und die umliegenden Dörfer zu erobern.
		#<EROBERT WEITERE STÄDTE>
		#<EROBERT DIE HEILIGE STADT>
		szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CITY_HEAD", (pCity.getName(), ))
		szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CITY_BODY", ("", ))
		PopUpDDS("Art/Scenarios/WegDerGoten/WDG02.dds",szTextHead,szTextBody)

		# Zoom zur neuen Hauptstadt
		CyCamera().JustLookAtPlot(pCity.plot())
		CyCamera().ZoomIn(0.5)

		# Heilige Stadt nur aufdecken
		pHolyCity = gc.getGame().getHolyCity(gc.getInfoTypeForString("RELIGION_NORDIC"))
		if pHolyCity is not None:
			doRevealPlot(0, pHolyCity.plot(), False)


#[QUEST] Wenn der Spieler einen Germanen erobert oder vasallisiert: (3x vorhanden: onCityAcquired, onPlayerKilled, onVassalState)
# egal ob es noch Einheiten gibt
	if iNewOwner == 0 and gc.getPlayer(iPreviousOwner).getNumCities() == 0:
		iConqueredPlayer = iPreviousOwner
		iPlayer = iNewOwner
		#Cherusker:
		#Gratulation! Ihr habt [get.Leadername] unter Euer Banner gezwungen. Er wird von nun an als Heeresführer an eurer Seite dienen.
		#<IHR ERHALTET 1 GENERAL "Arminius">
		if iConqueredPlayer == 1:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK", (gc.getPlayer(iConqueredPlayer).getName(), )))
			popupInfo.addPopup(iPlayer)
			
			pCity = gc.getPlayer(iPlayer).getCapitalCity()
			pNewUnit = gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_GREAT_GENERAL"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
			pNewUnit.setName("Arminius")

		#Warnen:
		#Gratulation! [get.Leadername] ist unterworfen. Seine besten Krieger kämpfen von nun an für uns.
		#<IHR ERHALTET 2 TEUTONEN>
		if iConqueredPlayer == 2:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN", (gc.getPlayer(iConqueredPlayer).getName(), )))
			popupInfo.addPopup(iPlayer)
			
			pCity = gc.getPlayer(iPlayer).getCapitalCity()
			gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		#Markomannen:
		#Gratulation! [get.Leadername] steht nun auf unserer Seite. Ein vor Jahren zu ihm übergelaufener Legionär schließt sich uns an.
		#<IHR ERHALTET 1 LEGIONÄR>
		if iConqueredPlayer == 3:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO", (gc.getPlayer(iConqueredPlayer).getName(), )))
			popupInfo.addPopup(iPlayer)
			
			pCity = gc.getPlayer(iPlayer).getCapitalCity()
			gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_LEGION2"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		#Hermunduren:
		#Gratulation! Ihr habt [get.Leadername] besiegt. Er zeigt uns den Weg zu seiner geheimen Schatzkammer.
		#<IHR ERHALTET 250 Gold>
		if iConqueredPlayer == 4:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN", (gc.getPlayer(iConqueredPlayer).getName(), )))
			popupInfo.addPopup(iPlayer)
			
			gc.getPlayer(iPlayer).changeGold(250)

		#[EVENT-10.4] Wenn der Spieler die alten Goten (Player 20) erobert hat -> DANN
		if iConqueredPlayer == 20:
			#Ausgezeichnet! Ihr habt die alte Heimat unter eure Kontrolle gebracht.
			#Nun lasst uns Vorbereitungen treffen, um die umliegenden Stämme zu unterwerfen. Wir sollten Spione ausbilden, um alle Windrichtungen zu erkunden. Und wir werden weitere Soldaten trainieren müssen, um zu gegebener Zeit mit einer großen Armee vor den Göttern nach Westen zu marschieren.
			#Alle großen Germanenstämme sollen hinter euch versammelt sein!
			#Denkt daran, schon früh Straßen in die weiten Wälder zu schlagen. Auch das wurde vom Ältesten immer vernachlässigt!
			#<VEREINT DIE GERMANENSTÄMME UNTER EUREM BANNER>
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_OLD_GOTHS", ("", )))
			popupInfo.addPopup(iPlayer)




#[QUEST] Wenn der Daker (oder sein Vasall) eine Stadt vom Vandalen erobert:
#[ABFRAGE] Hat der Spieler Frieden mit dem Vandalen? -> DANN
#Krakau 98/56 wird 1x kurz aufgedeckt
	if iPreviousOwner == 9 and (iNewOwner == 10 or iNewOwner == 11):
		if not gc.getTeam(gc.getPlayer(0).getTeam()).isAtWar(gc.getPlayer(9).getTeam()):
			#[get.Leadername] hat eine Stadt verloren! Er wird von den den [get.Civname] bedrängt. 
			#Können wir da vielleicht helfen? Wir wollen ja nicht noch eine starke Macht im Süden!
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_DAKER_CONQUER_VANDAL_CITY", (gc.getPlayer(9).getName(), gc.getPlayer(iNewOwner).getCivilizationDescriptionKey())))
			popupInfo.addPopup(iNewOwner)

			pCity = gc.getPlayer(iPreviousOwner).getCapitalCity()
			if pCity is not None:
				doRevealPlot(0, pCity.plot(), True)


#[QUEST ROM-A] Wenn Rom (oder sein Vasall) einem der GerVandanen die Hauptstadt erobert oder vasallisiert:
	if iPreviousOwner in lGerVandalen:
		if iNewOwner == 14 or gc.getTeam(gc.getPlayer(iNewOwner).getTeam()).isVassal(gc.getPlayer(14).getTeam()):
			lCapitals = ["Tulifurdum","Rostock","Virteburh","","Krakau"]
			if pCity.getName() in lCapitals:
				szTextHead = ""
				szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_CONQUERS_CAPITAL", (pCity.getName(),gc.getPlayer(iPreviousOwner).getName(),gc.getPlayer(iNewOwner).getName()))
				PopUpDDS("Art/Scenarios/WegDerGoten/WDG05.dds",szTextHead,szTextBody)


#[QUEST] Wenn Byzanz (oder sein Vasall) eine Stadt vom Daker erobert:
#[ABFRAGE] Hat der Spieler Frieden mit dem Daker?
#[ABFRAGE] Hat Rom noch Frieden mit Byzanz? -> DANN
#Sarmizetegusa 110/32 wird 1x kurz aufgedeckt
	if iPreviousOwner == 10:
		if iNewOwner == 12 or gc.getTeam(gc.getPlayer(iNewOwner).getTeam()).isVassal(gc.getPlayer(12).getTeam()):
			if not gc.getTeam(gc.getPlayer(10).getTeam()).isAtWar(gc.getPlayer(0).getTeam()):
				if not gc.getTeam(gc.getPlayer(12).getTeam()).isAtWar(gc.getPlayer(14).getTeam()):
					#[get.Leadername], der Unterhändler Roms, erobert Städte von [get.Leadername]. Also breiten sich die Römer jetzt auch im Osten aus. Wir sollten unsere Pläne anpassen...
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_BYZANZ_CONQUER_DAKER", (gc.getPlayer(iNewOwner).getName(), gc.getPlayer(iPreviousOwner).getName())))
					popupInfo.addPopup(0)

					pCity = gc.getPlayer(iPreviousOwner).getCapitalCity()
					if pCity is not None:
						doRevealPlot(0, pCity.plot(), True)


#Wenn der Hunne die erste Stadt einnimmt:
#Palast, Monument, Heldendenkmal setzen, der Hunne bekommt 1 Siedler
#Alle Religionen/Tempel entfernen
#Fremde Religion geben, Tempel der Religion setzen
	if iNewOwner == 19 and iNumCities == 1:
		pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_MONUMENT"), 1)

		# Die Hunnenhauptstadt bekommt 80% Kultur.
		iPreviousCulture = pCity.getCulture(iPreviousOwner) / 10
		pCity.setCulture(iPreviousOwner, iPreviousCulture * 2, 1)
		pCity.setCulture(iNewOwner, iPreviousCulture * 8, 1)




def onFirstContact(argsList):
	iTeamX, iHasMetTeamY = argsList

	# onFirstContact-Events gelten nur für den Goten
	if iTeamX != 0: return

	# Vandalen = 9
	lGerVandalen = [1,2,3,4,9]
	lGermanen = [1,2,3,4]

	#[QUEST] Wenn Kontakt mit einem Germanen entsteht, werden 1x kurz die Hauptstädte aller vier Germanen aufgedeckt:
	#Cherusker 60/70 - Warnen 70/82 - Markomannen 61/55 - Hermunduren 76/62
	if iHasMetTeamY in lGermanen:
		bFirstContact = True
		for iPlayer in lGermanen:
			if gc.getTeam(gc.getPlayer(iTeamX).getTeam()).isHasMet(gc.getPlayer(iHasMetTeamY).getTeam()):
				bFirstContact = False
				break

		if bFirstContact:
			for iPlayer in lGermanen:
				pCity = gc.getPlayer(iPlayer).getCapitalCity()
				if pCity is not None:
					doRevealPlot(0, pCity.plot(), True)
					# for PAE's black fog of war (falls der Plot immer sichtbar sein soll)
					#CvUtil.addScriptData(plot, "H", "X")
			
			#Ihr habt [get.Leadername] getroffen.
			#Wir sollten alle vier führenden Germanenstämme unter unserer Flagge vereinen, um der römischen Bedrohung ein geeintes Reich entgegenzustellen.
			#<EROBERT ODER VASALLISIERT ALLE 4 GERMANENSTÄMME>
			if gc.getPlayer(iTeamX).isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_GERMANEN", (gc.getPlayer(iHasMetTeamY).getName(), )))
				popupInfo.addPopup(iTeamX)


#[EVENT-20.1] Wenn Kontakt zum Vandalen (Player 9) entsteht:
	#Erstellen einer aktuellen Punktliste der GerVandanen.
	#[ABFRAGE] Steht der Vandale im Mittelfeld? -> DANN
	# Die Hauptstadt der Vandalen [get.Capitalplot] wird 1x aufgedeckt
	if iHasMetTeamY == 9:
		iScoreLast = 0
		iScoreBest = 0
		for iPlayer in lGerVandalen:
			if gc.getPlayer(iPlayer).isAlive():
				if iScoreLast == 0 or CyGame().getPlayerScore(iPlayer) < iScoreLast:
					iScoreLast = CyGame().getPlayerScore(iPlayer)
				if CyGame().getPlayerScore(iPlayer) > iScoreBest:
					iScoreBest = CyGame().getPlayerScore(iPlayer)

		if gc.getPlayer(iTeamX).isHuman():
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				#Ihr habt die Vandalen getroffen. Sie sind ein verwandtes Volk im Süden, nehmen jedoch nur unregelmäßig am Thing teil.
				#Unser Fokus liegt zwar im Westen, aber vielleicht lohnt es sich, [get.Leadername] als Vasall zu gewinnen? Es müsste allerdings schnell gehen, damit die Germanen im Westen nicht zu stark werden.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VANDALEN_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				#Ihr habt [get.Leadername] getroffen. Die Vandalen sind ein verwandtes Volk im Süden, nehmen aber nur unregelmäßig am Thing teil. 
				#Man darf sie jedoch keinesfalls unterschätzen, sie sind unberechenbar und neigen dazu, unüberlegte Entscheidungen zu treffen Behaltet sie im Auge und seid bereit, falls sie sich in unsere Richtung ausbreiten.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VANDALEN_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				#Ihr habt [get.Leadername] getroffen. Die Vandalen sind ein verwandtes Volk im Süden, nehmen aber nur unregelmäßig am Thing teil. 
				#Für unsere Pläne spielen sie im Moment noch keine Rolle. Behaltet sie jedoch im Auge, falls sie mächtiger werden.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VANDALEN_2", (gc.getPlayer(iHasMetTeamY).getName(), ))

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(szText)
				popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)


#[EVENT-21.1] Wenn Kontakt zum Warnen (Player 2) entsteht:
	#Erstellen einer aktuellen Punktliste der GerVandanen.
	#[ABFRAGE] Ist der Warne Erster? -> DANN (A)
	#[ABFRAGE] Steht der Warne im Mittelfeld? -> DANN (B)
	#[ABFRAGE] Ist der Warne Letzter? -> DANN (C)
	#Die Hauptstadt der Warnen [get.Capitalplot] wird 1x aufgedeckt
	if iHasMetTeamY == 2:
		iScoreLast = 0
		iScoreBest = 0
		for iPlayer in lGerVandalen:
			if gc.getPlayer(iPlayer).isAlive():
				if iScoreLast == 0 or CyGame().getPlayerScore(iPlayer) < iScoreLast:
					iScoreLast = CyGame().getPlayerScore(iPlayer)
				if CyGame().getPlayerScore(iPlayer) > iScoreBest:
					iScoreBest = CyGame().getPlayerScore(iPlayer)

		if gc.getPlayer(iTeamX).isHuman():
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist schon durch seine Körpergröße eine beeindruckende Persönlichkeit, aber seine Stimme übertrifft diesen Eindruck noch. Wenn er das Wort beim Thing erhebt, kann er sich der Aufmerksamkeit aller Anwesenden sicher sein!
				#Die Warnen sind eine ernstzunehmende Macht im Norden, die wir auf unserer Seite haben sollten. Womöglich sogar auf friedliche Weise?
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_WARNEN_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist trotz seiner Größe ein eher ruhiger Bursche aus dem Norden. Er trinkt viel und redet laut, aber beim Thing enthält er sich meist der Stimme und bekommt kein Wort heraus.
				#Könnte er vielleicht ein erstes Ziel sein? Mit seinem Land, oder ihm als Vasall, würden wir die gesamte Ostsee kontrollieren.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_WARNEN_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				#[get.Leadername] ist eine beeindruckende Persönlichkeit. Nicht nur was seine Körpergröße angeht, auch seine Stimme kann Lawinen auslösen! Beim Thing ist er jedoch eher zurückhaltend, überlässt anderen die Entscheidung.
				#Für unser Vorhaben Germanien zu vereinen spielt er eine entscheidende Rolle, da er mit uns zusammen die Ostsee kontrolliert. Wir sollten Spione schicken, um seine Stärke einzuschätzen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_WARNEN_2", (gc.getPlayer(iHasMetTeamY).getName(), ))

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(szText)
				popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)


#[EVENT-22.1] Wenn Kontakt zum Hermunduren (Player4) entsteht:
	#Erstellen einer aktuellen Punktliste der GerVandanen.
	#[ABFRAGE] Ist der Hermundure Erster? -> DANN (A)
	#[ABFRAGE] Steht der Hermundure im Mittelfeld? -> DANN (B)
	#[ABFRAGE] Ist der Hermundure Letzter? -> DANN (C)
	#Die Hauptstadt der Hermunduren [get.Capitalplot] wird 1x aufgedeckt
	if iHasMetTeamY == 4:
		iScoreLast = 0
		iScoreBest = 0
		for iPlayer in lGerVandalen:
			if gc.getPlayer(iPlayer).isAlive():
				if iScoreLast == 0 or CyGame().getPlayerScore(iPlayer) < iScoreLast:
					iScoreLast = CyGame().getPlayerScore(iPlayer)
				if CyGame().getPlayerScore(iPlayer) > iScoreBest:
					iScoreBest = CyGame().getPlayerScore(iPlayer)

		if gc.getPlayer(iTeamX).isHuman():
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist ein erfahrener Mann, dessen Wort beim Thing hohes Gewicht hat. Die Legende, dass er als Junge einen Ur mit bloßen Händen erlegte, eilt ihm voraus. Auch heute noch bewegt er sich trotz seines Alters geschmeidig wie ein Fuchs.
				#Auf die Hermunduren müsst ihr ein Auge haben. Vielleicht können wir friedlich miteinander auskommen und dennoch die Germanenstämme vereinen?
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_HERMUN_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist in seinem fortgeschrittenen Alter immer noch ein angesehener Redner beim Thing. Jedoch merkt man wie seine Kräfte langsam schwinden. Die Legende, dass er als Junge ganz alleine einen Ur erlegt haben soll, glaubt heute keiner mehr.
				#Wir sollten sein Reich unter unsere Kontrolle bringen! Die Entscheidung, ob er als euer Vasall an Altersschwäche stirbt oder ehrenhaft im Kampf fällt, bleibt euch überlassen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_HERMUN_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				#[get.Leadername] ist ein erfahrener Mann, dessen Wort beim Thing durchaus gehört wird. Die Legende, dass er als Junge einen Ur nur mit seinem Messer erlegt haben soll, ist nicht bestätigt. Aber auch heute noch bewegt er sich trotz seines Alters geschmeidig wie ein Fuchs.
				#Wir sollten Spione schicken, um Informationen über die wahre Stärke der Hermunduren zu erhalten. Wir sollten Spione schicken, um seine Stärke einzuschätzen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_HERMUN_2", (gc.getPlayer(iHasMetTeamY).getName(), ))

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(szText)
				popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)


#[EVENT-23.1] Wenn Kontakt zum Cherusker (Player1) entsteht:
	#Erstellen einer aktuellen Punktliste der GerVandanen.
	#[ABFRAGE] Ist der Cherusker Erster? -> DANN (A)
	#[ABFRAGE] Steht der Cherusker im Mittelfeld? -> DANN (B)
	#[ABFRAGE] Ist der Cherusker Letzter? -> DANN (C)
	#Die Hauptstadt der Cherusker [get.Capitalplot] wird 1x aufgedeckt
	if iHasMetTeamY == 1:
		iScoreLast = 0
		iScoreBest = 0
		for iPlayer in lGerVandalen:
			if gc.getPlayer(iPlayer).isAlive():
				if iScoreLast == 0 or CyGame().getPlayerScore(iPlayer) < iScoreLast:
					iScoreLast = CyGame().getPlayerScore(iPlayer)
				if CyGame().getPlayerScore(iPlayer) > iScoreBest:
					iScoreBest = CyGame().getPlayerScore(iPlayer)

		if gc.getPlayer(iTeamX).isHuman():
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist ein erfahrener Mann, dessen Wort beim Thing hohes Gewicht hat. Die Legende, dass er als Junge einen Ur mit bloßen Händen erlegte, eilt ihm voraus. Auch heute noch bewegt er sich trotz seines Alters geschmeidig wie ein Fuchs.
				#Auf die Hermunduren müsst ihr ein Auge haben. Vielleicht können wir friedlich miteinander auskommen und dennoch die Germanenstämme vereinen?
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_CHERUSK_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist in seinem fortgeschrittenen Alter immer noch ein angesehener Redner beim Thing. Jedoch merkt man wie seine Kräfte langsam schwinden. Die Legende, dass er als Junge ganz alleine einen Ur erlegt haben soll, glaubt heute keiner mehr.
				#Wir sollten sein Reich unter unsere Kontrolle bringen! Die Entscheidung, ob er als euer Vasall an Altersschwäche stirbt oder ehrenhaft im Kampf fällt, bleibt euch überlassen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_CHERUSK_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				#[get.Leadername] ist ein erfahrener Mann, dessen Wort beim Thing durchaus gehört wird. Die Legende, dass er als Junge einen Ur nur mit seinem Messer erlegt haben soll, ist nicht bestätigt. Aber auch heute noch bewegt er sich trotz seines Alters geschmeidig wie ein Fuchs.
				#Wir sollten Spione schicken, um Informationen über die wahre Stärke der Hermunduren zu erhalten. Wir sollten Spione schicken, um seine Stärke einzuschätzen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_CHERUSK_2", (gc.getPlayer(iHasMetTeamY).getName(), ))

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(szText)
				popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)


#[EVENT-24.1] Wenn Kontakt zum Markomannen (Player3) entsteht:
	#Erstellen einer aktuellen Punktliste der GerVandanen.
	#[ABFRAGE] Ist der Markomanne Erster? -> DANN (A)
	#[ABFRAGE] Steht der Markomanne im Mittelfeld? -> DANN (B)
	#[ABFRAGE] Ist der Markomanne Letzter? -> DANN (C)
	#Die Hauptstadt der Markomannen [get.Capitalplot] wird 1x aufgedeckt
	if iHasMetTeamY == 3:
		iScoreLast = 0
		iScoreBest = 0
		for iPlayer in lGerVandalen:
			if gc.getPlayer(iPlayer).isAlive():
				if iScoreLast == 0 or CyGame().getPlayerScore(iPlayer) < iScoreLast:
					iScoreLast = CyGame().getPlayerScore(iPlayer)
				if CyGame().getPlayerScore(iPlayer) > iScoreBest:
					iScoreBest = CyGame().getPlayerScore(iPlayer)

		if gc.getPlayer(iTeamX).isHuman():
			if iScoreBest == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist ein erfahrener Mann, dessen Wort beim Thing hohes Gewicht hat. Die Legende, dass er als Junge einen Ur mit bloßen Händen erlegte, eilt ihm voraus. Auch heute noch bewegt er sich trotz seines Alters geschmeidig wie ein Fuchs.
				#Auf die Hermunduren müsst ihr ein Auge haben. Vielleicht können wir friedlich miteinander auskommen und dennoch die Germanenstämme vereinen?
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_MARKO_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
			elif iScoreLast == CyGame().getPlayerScore(iHasMetTeamY):
				#[get.Leadername] ist in seinem fortgeschrittenen Alter immer noch ein angesehener Redner beim Thing. Jedoch merkt man wie seine Kräfte langsam schwinden. Die Legende, dass er als Junge ganz alleine einen Ur erlegt haben soll, glaubt heute keiner mehr.
				#Wir sollten sein Reich unter unsere Kontrolle bringen! Die Entscheidung, ob er als euer Vasall an Altersschwäche stirbt oder ehrenhaft im Kampf fällt, bleibt euch überlassen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_MARKO_3", (gc.getPlayer(iHasMetTeamY).getName(), ))
			else:
				#[get.Leadername] ist ein erfahrener Mann, dessen Wort beim Thing durchaus gehört wird. Die Legende, dass er als Junge einen Ur nur mit seinem Messer erlegt haben soll, ist nicht bestätigt. Aber auch heute noch bewegt er sich trotz seines Alters geschmeidig wie ein Fuchs.
				#Wir sollten Spione schicken, um Informationen über die wahre Stärke der Hermunduren zu erhalten. Wir sollten Spione schicken, um seine Stärke einzuschätzen.
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_MARKO_2", (gc.getPlayer(iHasMetTeamY).getName(), ))

				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(szText)
				popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)


#[QUEST] Wenn Kontakt zum Gallier entsteht:
#Lutetia 32/49 wird 1x kurz aufgedeckt
	if iHasMetTeamY == 6:
		# Hat Gallien Krieg mit Rom?
		if gc.getTeam(gc.getPlayer(6).getTeam()).isAtWar(gc.getPlayer(14).getTeam()):
			szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_GALLIA_1", (gc.getPlayer(iHasMetTeamY).getName(), ))
		else:
			szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_GALLIA_2", (gc.getPlayer(iHasMetTeamY).getName(), ))
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(szText)
		popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)


#[QUEST] Wenn Kontakt zum Daker oder seinem Vasall entsteht:
#Die [get.civname] sind ein fremdes Volk von weit aus den südlichen Wäldern. Solange sie nicht zu mächtig werden, 
#müssen wir ihnen keine Bachtung schenken. Es sei denn, ihr habt andere Pläne.
	if iHasMetTeamY == 10 or iHasMetTeamY == 11:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_DAKER", (gc.getPlayer(iHasMetTeamY).getCivilizationDescriptionKey(), )))
		popupInfo.addPopup(iTeamX)


#[QUEST] Wenn Kontakt zu Rom entsteht:
#Rom 70/11 wird 1x kurz aufgedeckt
#Das ist er also: [get.Leadername]! Er ist unersättlich, seine Legionen bedrohen die gesamte zivilisiert Welt! 
#Auch wenn es einige geben mag die meinen, Rom wäre die Zivilisation, wir dagegen seien Barbaren. 
#Solche Leute werden aber meist direkt aus der Wirtschaft geprügelt...
	if iHasMetTeamY == 14:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_ROME", (gc.getPlayer(iHasMetTeamY).getName(), )))
		popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)

#[QUEST] Wenn Kontakt zu einem Vasall Roms entsteht:
#[DARF ÖFTER KOMMEN]
#[ABFRAGE]Hat Rom noch Frieden mit Byzanz? -> DANN
	if gc.getTeam(gc.getPlayer(iHasMetTeamY).getTeam()).isVassal(gc.getPlayer(14).getTeam()):
		if not gc.getTeam(14).isAtWar(12):
			#Ihr habt [get.Leadername] getroffen, ein Vasall von [get.Leadername] (Rom). Solange er nicht frei entscheiden kann, ist er für uns uninteressant.
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VASSAL_OF_ROME", (gc.getPlayer(iHasMetTeamY).getName(), gc.getPlayer(14).getName())))
			popupInfo.addPopup(iTeamX)


#[QUEST] Wenn Kontakt zu Byzanz entsteht:
#Byzanz 134/7 wird 1x kurz aufgedeckt
#Ihr habt [get.Leadername] getroffen. Er hat seinen Palast in Byzanz und ist ein enger Vertrauter Roms. Im Prinzip verwaltet er für 
#[get.Leadername] (Rom) nur die östlichen Provinzen. Die Wahrscheinlichkeit, ihn auf unsere Seite zu bringen, ist im Moment sehr gering...
	if iHasMetTeamY == 12:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_BYZANZ", (gc.getPlayer(iHasMetTeamY).getName(), gc.getPlayer(14).getName())))
		popupInfo.addPopup(iTeamX)

		pCity = gc.getPlayer(iHasMetTeamY).getCapitalCity()
		if pCity is not None:
			doRevealPlot(0, pCity.plot(), True)

#[QUEST] Wenn Kontakt zu einem Vasall von Byzanz entsteht:
#Ihr habt [get.Leadername] getroffen, ein Vasall von [get.Leadername] (Byzanz). Solange er nicht frei entscheiden kann, ist er für uns uninteressant.
	if gc.getTeam(gc.getPlayer(iHasMetTeamY).getTeam()).isVassal(gc.getPlayer(12).getTeam()):
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_FIRST_CONTACT_VASSAL_OF_BYZANZ", (gc.getPlayer(iHasMetTeamY).getName(), gc.getPlayer(12).getName())))
		popupInfo.addPopup(iTeamX)



def onCombatResult(pWinner, pLoser):
	iWinner = pWinner.getOwner()
	iLoser = pLoser.getOwner()
#[EVENT-10.2] Wenn der Älteste stirbt:
	#"The Elder" ist Stammesfürst mit General der Alten Goten (Player 20) in Hagelsberg. Wenn der besiegt ist:
	#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
	#[ABFRAGE] Ist er irgendwo anders gestorben? -> DANN (B)
	#(A)
	#Der Älteste ist besiegt! Damit hat [get.LeadernamePlayer20] seine besten Kämpfer verloren.
	#Und wir konnten seinen engsten Vertrauten festnehmen. Oswald ist ein viel gereister Mann, der sich in den Wäldern bestens auskennt. Und er ist weise genug, die richtige Entscheidung zu treffen. Bevor er am Galgenbaum endet, kniet er nieder und schwört euch die ewige Treue.
	#Ihr nehmt ihn gerne auf, von seinem Wissen und seinen Fähigkeiten können wir nur profitieren.
	#<IHR ERHALTET 1 GROSSER SPION> "Oswald"
	#KAMERA ZOOM AUF DEN ORT DES KAMPFES
	#Großer Spion "Oswald" wird erstellt. Er bekommt die Beförderung Wald III (doppelte Fortbewegung im Wald)
	#(B)
	#Der Älteste ist gefallen! Wo auch immer er sich versteckt hatte, sein Schicksal hat ihn eingeholt!
	iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
	if iLoser == 20 and pLoser.isHasPromotion(iPromoLeader) and (pLoser.getName() == "The Elder" or pLoser.getScriptData() == "The Elder"):
		#[ABFRAGE] Hat der Spieler ihn besiegt? -> DANN (A)
		if iWinner == 0:
			pNewUnit = gc.getPlayer(iWinner).initUnit(gc.getInfoTypeForString("UNIT_GREAT_SPY"), pWinner.getX(), pWinner.getY(), UnitAITypes.UNITAI_SPY, DirectionTypes.DIRECTION_SOUTH)
			pNewUnit.setName("Oswald")
			pNewUnit.setHasPromotion(gc.getInfoTypeForString("PROMOTION_COMMANDO"), True)
			CyCamera().LookAtUnit(pNewUnit)

			if gc.getPlayer(iWinner).isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_THE_ELDER", (gc.getPlayer(iLoser).getName(), )))
				popupInfo.addPopup(iWinner)

		#[ABFRAGE] Ist er irgendwo anders gestorben? -> DANN (B)
		else:
			if gc.getPlayer(0).isHuman():
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_THE_ELDER", (gc.getPlayer(iLoser).getName(), )))
				popupInfo.addPopup(0)

#[EVENT-11.1 Wenn Alarich stirbt:
	if iLoser == 0 and pLoser.isHasPromotion(iPromoLeader) and (pLoser.getName() == "Alarich" or pLoser.getScriptData() == "Alarich"):
		#Die Startarmee des Spielers wird von Stammesfürst mit General "Alarich" angeführt.
		#Nach dessen Tod gibt es einen neuen Leader der Goten (X oder Y)
		#<[get.Leadername] ÜBERNIMMT DIE FÜHRUNG DER GOTEN>

		#Der Nachfolger von Alarich I. als König der Westgoten war sein Schwager Ataulf.
		iLeader = gc.getInfoTypeForString("LEADER_TEUTOBOD")
		gc.getPlayer(iLoser).changeLeader(iLeader) # change to XML leader
		gc.getPlayer(iLoser).setName("Ataulf") # Leader's name

		#Der Herr über das Gotenreich ist gefallen! Ihr seid tot!
		#Zeit für Trauer bleibt jedoch nicht viel, das Leben muss weitergehen. Zu euren Ehren wird in [get.capitalname] ein Monument errichtet, wie es noch keins zuvor gab. Ein riesiger gehauener Stein, der mit einer Inschrift an Alarich den Goten erinnert.
		#Doch wer soll eure Nachfolge antreten? Die Adligen kommen zusammen, um eine Entscheidung zu treffen.
		#[AUSWAHL] X oder Y

		#[ABFRAGE] Gibt es schon eine Hauptstadt? -> DANN
		#<DIE STELE DES ALARICH WIRD IN [get.Capitalname] ERRICHTET> (Obelisk)
		pCity = gc.getPlayer(iLoser).getCapitalCity()
		if pCity.isNone():
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_HEAD", ("", ))
			szTextBody = ""
			PopUpDDS("Art/Scenarios/WegDerGoten/WDG07.dds",szTextHead,szTextBody)
		else:
			pCity.setNumRealBuilding(gc.getInfoTypeForString("BUILDING_OBELISK"), 1)
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_HEAD", ("", ))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ALARICH_BODY", ("", ))
			PopUpDDS("Art/Scenarios/WegDerGoten/WDG07.dds",szTextHead,szTextBody)




#[QUEST] Wenn der Spieler einen Germanen erobert oder vasallisiert: (3x vorhanden: onCityAcquired, onPlayerKilled, onVassalState)
def onPlayerKilled(iConqueredPlayer):
	iPlayer = gc.getGame().getActivePlayer()
	if iPlayer != 0: return

	#Cherusker:
	#Gratulation! Ihr habt [get.Leadername] unter Euer Banner gezwungen. Er wird von nun an als Heeresführer an eurer Seite dienen.
	#<IHR ERHALTET 1 GENERAL "Arminius">
	if iConqueredPlayer == 1:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK", (gc.getPlayer(iConqueredPlayer).getName(), )))
		popupInfo.addPopup(iPlayer)
		
		pCity = gc.getPlayer(iPlayer).getCapitalCity()
		pNewUnit = gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_GREAT_GENERAL"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
		pNewUnit.setName("Arminius")

	#Warnen:
	#Gratulation! [get.Leadername] ist unterworfen. Seine besten Krieger kämpfen von nun an für uns.
	#<IHR ERHALTET 2 TEUTONEN>
	if iConqueredPlayer == 2:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN", (gc.getPlayer(iConqueredPlayer).getName(), )))
		popupInfo.addPopup(iPlayer)
		
		pCity = gc.getPlayer(iPlayer).getCapitalCity()
		gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
		gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

	#Markomannen:
	#Gratulation! [get.Leadername] steht nun auf unserer Seite. Ein vor Jahren zu ihm übergelaufener Legionär schließt sich uns an.
	#<IHR ERHALTET 1 LEGIONÄR>
	if iConqueredPlayer == 3:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO", (gc.getPlayer(iConqueredPlayer).getName(), )))
		popupInfo.addPopup(iPlayer)
		
		pCity = gc.getPlayer(iPlayer).getCapitalCity()
		gc.getPlayer(iPlayer).initUnit(gc.getInfoTypeForString("UNIT_LEGION2"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

	#Hermunduren:
	#Gratulation! Ihr habt [get.Leadername] besiegt. Er zeigt uns den Weg zu seiner geheimen Schatzkammer.
	#<IHR ERHALTET 250 Gold>
	if iConqueredPlayer == 4:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN", (gc.getPlayer(iConqueredPlayer).getName(), )))
		popupInfo.addPopup(iPlayer)
		
		gc.getPlayer(iPlayer).changeGold(250)



def onVassalState(argsList):
	iMaster, iVassal, bVassal = argsList

	lGerVandalen = [1,2,3,4,9]

	#[QUEST] Wenn der Spieler einen Germanen erobert oder vasallisiert: (3x vorhanden: onCityAcquired, onPlayerKilled, onVassalState)
	if iMaster == 0 and bVassal:
		#Cherusker:
		#Gratulation! Ihr habt [get.Leadername] unter Euer Banner gezwungen. Er wird von nun an als Heeresführer an eurer Seite dienen.
		#<IHR ERHALTET 1 GENERAL "Arminius">
		if iVassal == 1:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_CHERUSK", (gc.getPlayer(iVassal).getName(), )))
			popupInfo.addPopup(0)

			pCity = gc.getPlayer(iVassal).getCapitalCity()
			pNewUnit = gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_GREAT_GENERAL"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_GENERAL, DirectionTypes.DIRECTION_SOUTH)
			pNewUnit.setName("Arminius")

		#Warnen:
		#Gratulation! [get.Leadername] ist unterworfen. Seine besten Krieger kämpfen von nun an für uns.
		#<IHR ERHALTET 2 TEUTONEN>
		if iVassal == 2:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_WARNEN", (gc.getPlayer(iVassal).getName(), )))
			popupInfo.addPopup(0)
			
			pCity = gc.getPlayer(iVassal).getCapitalCity()
			gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_TEUTONEN"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		#Markomannen:
		#Gratulation! [get.Leadername] steht nun auf unserer Seite. Ein vor Jahren zu ihm übergelaufener Legionär schließt sich uns an.
		#<IHR ERHALTET 1 LEGIONÄR>
		if iVassal == 3:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_MARKO", (gc.getPlayer(iVassal).getName(), )))
			popupInfo.addPopup(0)
			
			pCity = gc.getPlayer(iVassal).getCapitalCity()
			gc.getPlayer(0).initUnit(gc.getInfoTypeForString("UNIT_LEGION2"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		#Hermunduren:
		#Gratulation! Ihr habt [get.Leadername] besiegt. Er zeigt uns den Weg zu seiner geheimen Schatzkammer.
		#<IHR ERHALTET 250 Gold>
		if iVassal == 4:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CONQUER_HERMUN", (gc.getPlayer(iVassal).getName(), )))
			popupInfo.addPopup(0)
			
			gc.getPlayer(0).changeGold(250)


	#[QUEST] Wenn sich ein Vasall von Rom lossagt:
	#[get.Leadername] hat sich von [get.Leadername] (Rom) losgesagt und ist wieder frei. Wir sollten umgehend einen Boten schicken!
	if iMaster == 14 and not bVassal:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_LOST_VASSAL", (gc.getPlayer(iVassal).getName(),gc.getPlayer(iMaster).getName())))
			popupInfo.addPopup(0)


	#[QUEST ROM-A] Wenn Rom (oder sein Vasall) einem der GerVandanen die Hauptstadt erobert oder vasallisiert:
	if bVassal and iVassal in lGerVandalen:
		if iMaster == 14 or gc.getTeam(gc.getPlayer(iMaster).getTeam()).isVassal(gc.getPlayer(14).getTeam()):
			szTextHead = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_VASSALS_GERVANDALS_HEAD", ("", ))
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_VASSALS_GERVANDALS_BODY", ("", ))
			PopUpDDS("Art/Scenarios/WegDerGoten/WDG05.dds",szTextHead,szTextBody)

	#[QUEST] Wenn sich ein Vasall von Byzanz lossagt:
	#[get.Leadername] hat sich von [get.Leadername] (Byzanz) losgesagt und ist wieder frei. Wir sollten umgehend einen Boten schicken!
	if iMaster == 12 and not bVassal:
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_BYZANZ_LOST_VASSAL", (gc.getPlayer(iVassal).getName(),gc.getPlayer(iMaster).getName())))
			popupInfo.addPopup(0)



def onChangeWar(argsList):
	bIsWar, iTeam, iRivalTeam = argsList
	lGerVandalen = [1,2,3,4,9]
	lGermanen = [1,2,3,4]
	# wenn Krieg erklärt wird
	if bIsWar:
		#Wenn einer der GerVandalen dem Spieler Krieg erklärt:
		if iTeam in lGerVandalen and iRivalTeam == 0:
			for iPlayer in lGerVandalen:
				if gc.getPlayer(iPlayer).getTeam() == iTeam:
					iPlayerDeclaredWar = iPlayer
					break
			#[get.Leadername] kann es wohl nicht erwarten unter Euch zu dienen. Ihr lasst die Truppen sammeln. Die [get.Civname] werden sich schon bald Goten nennen!
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GER_DECLARE_WAR_GOTEN", (gc.getPlayer(iPlayerDeclaredWar).getName(), gc.getPlayer(iPlayerDeclaredWar).getCivilizationDescriptionKey())))
			popupInfo.addPopup(0)

		#[QUEST] Wenn der Gallier einem der 4 Germanen Krieg erklärt:
		if iTeam == 6 and iRivalTeam in lGermanen:
			#[ABFRAGE] Hat der Spieler Frieden mit dem betroffenen Germanen? -> DANN
			#[get.Leadername] wird von Galliern aus dem Westen angegriffen! Auch das noch, können wir was tun?
			if not gc.getTeam(gc.getPlayer(0).getTeam()).isAtWar(iRivalTeam):
				for iPlayer in lGermanen:
					if gc.getPlayer(iPlayer).getTeam() == iRivalTeam:
						iPlayerVictim = iPlayer
						break
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GALLIA_DECLARES_WAR_GERMANIA", (gc.getPlayer(iPlayerVictim).getName(), )))
				popupInfo.addPopup(0)

		#[QUEST] Wenn Rom einem der GerVandanen Krieg erklärt:
		#Die Römer mischen sich in unsere Angelegenheiten ein, sie haben [get.Leadername] den Krieg erklärt! Das ist eine Provokation, 
		#auf die wir reagieren sollten. Vielleicht können wir [get.Leadername] zu Hilfe eilen, bzw. dem Römer wenigstens zuvorzukommen?
		if iTeam == 14 and iRivalTeam in lGerVandalen:
				popupInfo = CyPopupInfo()
				popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
				popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_DECLARES_WAR_GERVANDALS", (gc.getPlayer(iRivalTeam).getName(), )))
				popupInfo.addPopup(0)

#[EVENT-27.1] Wenn einer der GerVandanen dem Römer Krieg erklärt:
		#[QUEST] Wenn einer der GerVandanen dem Römer (oder seinen Vasallen) Krieg erklärt:
		#[DARF ÖFTER KOMMEN]
		#[ABFRAGE] Hat der Spieler Frieden mit dem angreifenden GerVandanen? -> DANN
		#[get.Leadername] hat Rom den Krieg erklärt! Man muss ihm viel Glück wünschen.
		#Vielleicht können wir ihn unterstützen? Zumindest sollten wir unsere Pläne anpassen.
		if iTeam in lGerVandalen:
			if iRivalTeam == 14 or gc.getTeam(iRivalTeam).isVassal(gc.getPlayer(14).getTeam()):
				if not gc.getTeam(gc.getPlayer(0).getTeam()).isAtWar(iTeam):
					popupInfo = CyPopupInfo()
					popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
					popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GERVANDALS_DECLARES_WAR_ROME", (gc.getPlayer(iTeam).getName(), )))
					popupInfo.addPopup(0)

		#[QUEST ROM-C] Wenn Rom dem Spieler Krieg erklärt:
		if iTeam == 14 and iRivalTeam == 0:
			szTextHead = ""
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_ROME_DECLARES_WAR_GOTEN", (gc.getPlayer(iTeam).getName(), ))
			PopUpDDS("Art/Scenarios/WegDerGoten/WDG05.dds",szTextHead,szTextBody)



def onEndPlayerTurn(iPlayer, iGameTurn):
	pPlayer = gc.getPlayer(iPlayer)

	#[QUEST] Ab 350 n.Chr. gibt es jedes Jahr eine 2% Chance, dass die Hunnen kommen (also innerhalb von 50 Jahren):
	#[ABFRAGE] Welchen Nationen gehören die Städte im Osten (Muss man noch sehen, welche).
	#Attila spawnt mit seiner Armee zufällig an einem von mehreren möglichen Punkten. Er hat schlechtes Verhältnis und Krieg mit den Goten und allen, die in der Abfrage sind.
	#Attila bekommt alle Städte im Osten aufgedeckt.
	#Der Spieler bekommt das Feld aufgedeckt, wo er spawnt, sieht die Armee.
	
	#5-10 Runden vorher gibt es eine Warnung: Die Hunnen kommen bald
	if iPlayer == 19 and gc.getGame().getGameTurnYear() == 349:
		popupInfo = CyPopupInfo()
		popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
		popupInfo.setText(CyTranslator().getText("Die Hunnen kommen bald!", ("", ))) # XXX
		popupInfo.addPopup(0)
	
	if iPlayer == 0 and gc.getGame().getGameTurnYear() > 350:
		iHuns = 19 #TeamID

		if gc.getPlayer(iHuns).getNumCities() > 0: return

		iRand = CvUtil.myRandom(100, "WDG_Hunnen")
		if iRand < 2:

			#Herr, unsere Späher melden eine riesige Reiterarmee unbekannter Herkunft im Osten! Es sind die Hunnen.
			#Und sie werden von einem grimmig aussehenden Krieger geführt, der sich Attila nennt. Wir müssen uns schützen... etc.
			szTextHead = ""
			szTextBody = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_HUNNEN", ("", ))
			PopUpDDS("Art/Scenarios/WegDerGoten/WDG06.dds",szTextHead,szTextBody)

			lPlots = []
			iMapW = gc.getMap().getGridWidth()
			iMapH = gc.getMap().getGridHeight()
			iDarkIce = gc.getInfoTypeForString("FEATURE_DARK_ICE")
			iTundra = gc.getInfoTypeForString("TERRAIN_TUNDRA") # damit man eingrenzen kann, wo die Hunnen starten sollen
			for x in range(iMapW):
				for y in range(iMapH):
					if x > iMapW / 2 and y > iMapH / 2:
						loopPlot = gc.getMap().plot(x, y)
						if loopPlot is not None and not loopPlot.isNone():
							if loopPlot.getFeatureType() == iDarkIce or loopPlot.isWater():
								continue
							if loopPlot.getTerrainType() == iTundra and loopPlot.getOwner() == -1:
								lPlots.append(loopPlot)
			iRand = CvUtil.myRandom(len(lPlots), "WDG_Hunnen_Plot")
			pPlot = lPlots[iRand]

			iUnit = gc.getInfoTypeForString("UNIT_HEAVY_HORSEMAN_HUN")
			for _ in range(15):
				pNewUnit = gc.getPlayer(iHuns).initUnit(iUnit, pPlot.getX(), pPlot.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)
			CyCamera().LookAtUnit(pNewUnit)
			#CyCamera().ZoomIn(0.5)



#[EVENT-2.1] Christentum Gründung:
#Ab Jahr 5 v.Chr. gibt es eine 5% Chance, dass es entsteht (also innerhalb von 20 Jahren, NICHT Runden!)
#Entstehen soll es dann in Byzanz (80%) oder Rom (20%) -> DANN
def setChristentum():
		if CvUtil.myRandom(20, "WDG Christentum") != 1: return

		pCity = None
		iChance = CvUtil.myRandom(10, "WDG Christentum HolyCity")
		if iChance < 2:
			# Rom: x=70,y=11
			pPlot = plotXY(70, 11, 0, 0)
			if pPlot.isCity(): pCity = pPlot.getPlotCity()
		else:
			# Byzanz: x=134,y=7
			pPlot = plotXY(134, 7, 0, 0)
			if pPlot.isCity(): pCity = pPlot.getPlotCity()

		# 1. Heilige Stadt setzen
		if pCity is not None:
				gc.getGame().setHolyCity(gc.getInfoTypeForString("RELIGION_CHRISTIANITY"), pCity, True)

				# Es gibt Gerüchte, dass in [get.cityname] ein Kind geboren- und damit eine alte Prophezeiung erfüllt wurde... 
				# Es soll keinen sterblichen Vater haben, sondern von einem Gott gezeugt sein!
				szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CHRIST_SET", (pCity.getName(), ))
				PopUpDDS("Art/Scenarios/WegDerGoten/WDG03.dds","",szText)

				# 2. Religion den Barbaren zukommen (sonst kommt Religionswahl bei Theologie)
				pBarbTeam = gc.getTeam(gc.getPlayer(gc.getBARBARIAN_PLAYER()).getTeam())
				pBarbTeam.setHasTech(gc.getInfoTypeForString("TECH_THEOLOGY"), True, gc.getBARBARIAN_PLAYER(), True, False)



#[EVENT-2.2] Christentum verbreitet sich:
#Ab Gründung gibt es eine 2% Chance pro Jahr, dass die Verbreitung beginnt -> DANN
def doSpreadReligion():

		if CvUtil.myRandom(100, "WDG Christentum Verbreitung") < 2:

			iBuilding = gc.getInfoTypeForString("BUILDING_PROVINZPALAST")
			iChristentum = gc.getInfoTypeForString("RELIGION_CHRISTIANITY")
			iIslam = gc.getInfoTypeForString("RELIGION_ISLAM")
			iReligion = iChristentum

			if gc.getGame().isReligionFounded(iReligion):

				# Stadt suchen, die diese Religion hat
				lCities = []
				pCapitalCity = None
				iNumPlayers = gc.getMAX_PLAYERS()
				for i in range(iNumPlayers):
					loopPlayer = gc.getPlayer(i)
					if loopPlayer.isAlive():
						iNumCities = loopPlayer.getNumCities()
						for j in range(iNumCities):
							loopCity = loopPlayer.getCity(j)
							if loopCity is not None and not loopCity.isNone():
								if loopCity.isHasReligion(iReligion):
									lCities.append(loopCity)

				if len(lCities):
					pCity = lCities[CvUtil.myRandom(len(lCities), "doSpreadReligion_RandomCity")]
					if pCity is None or pCity.isNone(): return

					iX = pCity.getX()
					iY = pCity.getY()

					lCities = []
					iRange = 20
					iCityCheck = 0
					for i in range(-iRange, iRange+1):
						for j in range(-iRange, iRange+1):
							loopPlot = plotXY(iX, iY, i, j)
							if loopPlot.isCity():
								loopCity = loopPlot.getPlotCity()
								if loopCity.isConnectedTo(pCity) and not loopCity.isHasReligion(iReligion):
									if loopCity.isCapital() or loopCity.isHasBuilding(iBuilding):
										pCapitalCity = loopCity
									elif not loopCity.isHasReligion(iIslam):
										lCities.append(loopCity)

					# Christen auch über Handelswege verbreiten
					# ausser es wurde eine wichtige Stadt gefunden
					if pCapitalCity is None:
							iTradeRoutes = pCity.getTradeRoutes()
							for i in range(iTradeRoutes):
								loopCity = pCity.getTradeCity(i)
								if loopCity.isCapital() or loopCity.isHasBuilding(iBuilding):
									pCapitalCity = loopCity
									break
								elif not loopCity.isHasReligion(iReligion) and not loopCity.isHasReligion(iIslam):
									lCities.append(loopCity)

					# gefundene Hauptstadt immer konvertieren
					if not pCapitalCity is None:
						pCity = pCapitalCity

					elif len(lCities):
						iRand = CvUtil.myRandom(len(lCities), "doSpreadReligionChooseCity")
						pCity = lCities[iRand]

					pCity.setHasReligion(iReligion, 1, 1, 0)

					# Der neue Glaube, der vor Jahren in [get.cityname] begründet wurde, breitet sich weiter aus. 
					# Die Anhänger nennen sich Christen und sollen keine anderen Götter neben ihrem eigenen dulden...
					# Obwohl ihr Prophet am Kreuz gestorben ist, behaupten sie, er wandle dennoch unter ihnen.
					szText = CyTranslator().getText("TXT_KEY_MESSAGE_WDG_CHRIST_SPREAD", (gc.getGame().getHolyCity(iReligion).getName(), ))
					PopUpDDS("Art/Scenarios/WegDerGoten/WDG04.dds","",szText)


def onCityGrowth(pCity,iPlayer):
	global GotenCities3Pop6
	global GotenErsteProvinzstadt
	pPlayer = gc.getPlayer(iPlayer)

#[EVENT-12.2] Wenn der Spieler 3 Städte mit Größe 6 (Stadtstatus) hat:
	iBuilding = gc.getInfoTypeForString("BUILDING_STADT")
	if iPlayer == 0 and pPlayer.countNumBuildings(iBuilding) == 3 and not GotenCities3Pop6:
		GotenCities3Pop6 = True

		#[ABFRAGE] Lebt Alarich noch? -> DANN
		iRange = pPlayer.getNumUnits()
		for i in range(iRange):
			if pPlayer.getUnit(i) is not None:
				iPromoLeader = gc.getInfoTypeForString("PROMOTION_LEADER")
				if pPlayer.getUnit(i).isHasPromotion(iPromoLeader) and (pPlayer.getUnit(i).getName() == "Alarich" or pPlayer.getUnit(i).getScriptData() == "Alarich"):

					#+1 Zufriedenheit im Palast
					pCity = pPlayer.getCapitalCity()
					if not pCity.isNone():
						iBuildingClass = gc.getInfoTypeForString("BUILDINGCLASS_PROVINZPALAST")
						iBuildingHappiness = pCity.getBuildingHappyChange(iBuildingClass)
						pCity.setBuildingHappyChange(iBuildingClass, iBuildingHappiness + 1)

						if pPlayer.isHuman():
							popupInfo = CyPopupInfo()
							popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
							popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GOTEN_3POP6", ("", )))
							popupInfo.addPopup(iPlayer)
					return

#[EVENT-12.3] Wenn der Spieler seine erste Provinzstadt (Größe 12) hat -> DANN
	#1 Gaufürst wird erstellt (Auch wenn es schon einen gibt)
	if iPlayer == 0 and pCity.getPopulation() == 12 and not GotenErsteProvinzstadt:
		GotenErsteProvinzstadt = True

		pPlayer.initUnit(gc.getInfoTypeForString("UNIT_STATTHALTER_NORTH"), pCity.getX(), pCity.getY(), UnitAITypes.UNITAI_ATTACK, DirectionTypes.DIRECTION_SOUTH)

		#[get.cityname] ist zu erstaunlicher Größe herangewachsen. Einer der ansässigen Adligen erklärt sich bereit, die Verwaltung zu übernehmen.
		#<IHR ERHALTET 1 GAUFÜRST>
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GOTEN_ERSTEPROVINZSTADT", (pCity.getName(), )))
			popupInfo.addPopup(iPlayer)



def onBuildingBuilt(pCity, iPlayer, iBuildingType):
#[EVENT-12.4] Wenn der Spieler seinen ersten Provinzpalast baut -> DANN
	#KAMERA ZOOM AUF DIE STADT
	if iPlayer == 0 and iBuildingType == gc.getInfoTypeForString("BUILDING_PROVINZPALAST"):
		pPlayer = gc.getPlayer(iPlayer)
		pCapital = pPlayer.getCapitalCity()
		#Hier, von [get.cityname] aus wird unsere erste Provinz verwaltet.
		#Schon seit den Ahnen gilt: Mit der Entfernung zu [get.capitalname] nimmt die Motivation des Adels ab! Provinzpaläste sind der Schlüssel zu einem großen Reich. Von dort aus können Gaufürsten eures Vertrauens in der Gegend für Ruhe sorgen.
		if pPlayer.isHuman():
			popupInfo = CyPopupInfo()
			popupInfo.setButtonPopupType(ButtonPopupTypes.BUTTONPOPUP_TEXT)
			popupInfo.setText(CyTranslator().getText("TXT_KEY_MESSAGE_WDG_GOTEN_ERSTERPROVINZPALAST", (pCity.getName(),pCapital.getName())))
			popupInfo.addPopup(iPlayer)


def doRevealPlot(iTeam, pPlot, bZoom):
	iX = pPlot.getX()
	iY = pPlot.getY()
	for x in range(-1, 2):
		for y in range(-1, 2):
			loopPlot = plotXY(iX, iY, x, y)
			if loopPlot and not loopPlot.isNone():
				loopPlot.setRevealed(iTeam, True, False, -1)
	if bZoom:
		CyCamera().JustLookAtPlot(pPlot)
		#CyCamera().ZoomIn(0.5)


# PopUps mit dds-Bild
def PopUpDDS(ddsPIC, txtHEADER, txtBODY):
	screen = CyGInterfaceScreen("MainInterface", CvScreenEnums.MAIN_INTERFACE)
	iX = screen.getXResolution() / 2 - 200
	popupDDS = PyPopup.PyPopup(4000, EventContextTypes.EVENTCONTEXT_ALL) # 4000 = PopUpID
	#popupDDS.setSize(400,400) # (INT iXS, INT iYS) geht net
	popupDDS.setPosition(iX,40)
	popupDDS.setHeaderString(txtHEADER)
	popupDDS.addDDS(ddsPIC, 0, 0, 256, 256) # (dds, x, y, width: 360 max, height)
	popupDDS.setBodyString(txtBODY)
	popupDDS.launch()
