from CvPythonExtensions import (CyGlobalContext,
																PanelStyles, CyTranslator, PopupStates,
																WidgetTypes, FontTypes, TableStyles)
import CvUtil
if not CvUtil.isPitbossHost():
		from CvPythonExtensions import CyGInterfaceScreen
# import ScreenInput
import CvScreenEnums
import WBProjectScreen
import WBTeamScreen
import WBPlayerScreen
import WBPlayerUnits
import WBInfoScreen

# TODO remove
# DEBUG code for Python 3 linter
# unicode = str
# xrange = range

gc = CyGlobalContext()

iChangeType = 2
bApplyAll = False
bNoBarb = True
iSelectedEra = -1

# changed for PAE


class WBTechScreen:

		def __init__(self):
				self.iTable_Y = 110

		def interfaceScreen(self, iTeamX):
				screen = CyGInterfaceScreen("WBTechScreen", CvScreenEnums.WB_TECH)
				global iTeam
				global pTeam
				iTeam = iTeamX
				pTeam = gc.getTeam(iTeam)

				screen.setRenderInterfaceOnly(True)
				screen.addPanel("MainBG", u"", u"", True, False, -10, -10, screen.getXResolution() + 20, screen.getYResolution() + 20, PanelStyles.PANEL_STYLE_MAIN)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)

				screen.setText("WBTechExit", "Background", "<font=4>" + CyTranslator().getText("TXT_KEY_PEDIA_SCREEN_EXIT", ()).upper() + "</font>", CvUtil.FONT_RIGHT_JUSTIFY,
											 screen.getXResolution() - 30, screen.getYResolution() - 42, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1)
				screen.setLabel("TechHeader", "Background", u"<font=4b>" + CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()) + "</font>",
												CvUtil.FONT_CENTER_JUSTIFY, screen.getXResolution()/2, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				screen.addDropDownBoxGFC("CurrentTeam", 20, 20, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				for i in xrange(gc.getMAX_TEAMS()):
						loopTeam = gc.getTeam(i)
						if loopTeam.isAlive():
								iLeader = loopTeam.getLeaderID()
								sName = gc.getPlayer(iLeader).getName()
								if loopTeam.getNumMembers() > 1:
										sName += " (" + str(gc.getTeam(i).getNumMembers()) + " " + CyTranslator().getText("TXT_KEY_MEMBERS_TITLE", ()) + ")"
								screen.addPullDownString("CurrentTeam", sName, i, i, i == iTeam)

				screen.addDropDownBoxGFC("CurrentPage", 20, screen.getYResolution() - 42, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_PLAYER_DATA", ()), 0, 0, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_WB_TEAM_DATA", ()), 1, 1, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_PROJECT", ()), 2, 2, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_TECH", ()), 3, 3, True)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_PEDIA_CATEGORY_UNIT", ()) + " + " + CyTranslator().getText("TXT_KEY_CONCEPT_CITIES", ()), 4, 4, False)
				screen.addPullDownString("CurrentPage", CyTranslator().getText("TXT_KEY_INFO_SCREEN", ()), 11, 11, False)

				screen.addDropDownBoxGFC("TechEra", 20, self.iTable_Y - 30, screen.getXResolution()/5, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("TechEra", CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()), -1, -1, True)
				for i in xrange(gc.getNumEraInfos()):
						screen.addPullDownString("TechEra", gc.getEraInfo(i).getDescription(), i, i, i == iSelectedEra)

				sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_GAME_OPTION_NO_BARBARIANS", ()) + "</font>"
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if bNoBarb:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				screen.setText("NoBarbarians", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY,
											 screen.getXResolution() - 20, 20, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				sText = "<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYERS", ()),)) + "</font>"
				sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
				if bApplyAll:
						sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
				screen.setText("ApplyAll", "Background", sColor + sText + "</color>", CvUtil.FONT_RIGHT_JUSTIFY,
											 screen.getXResolution() - 20, 50, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				screen.addDropDownBoxGFC("ChangeType", screen.getXResolution() - 120, self.iTable_Y - 30, 100, WidgetTypes.WIDGET_GENERAL, -1, -1, FontTypes.GAME_FONT)
				screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_MODIFY", ("",)), 2, 2, 2 == iChangeType)
				screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_ADD", ()), 1, 1, 1 == iChangeType)
				screen.addPullDownString("ChangeType", CyTranslator().getText("TXT_KEY_WB_CITY_REMOVE", ()), 0, 0, 0 == iChangeType)
				sText = CyTranslator().getText("[COLOR_SELECTED_TEXT]", ()) + "<font=4b>" + CyTranslator().getText("TXT_KEY_WB_CITY_ALL", ()) + " (+/-)</color></font>"
				screen.setText("TechAll", "Background", sText, CvUtil.FONT_RIGHT_JUSTIFY, screen.getXResolution() - 120, self.iTable_Y - 30, -0.1, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				self.createTechList()
				self.placeTechs()

		def placeTechs_Platy(self):
				screen = CyGInterfaceScreen("WBTechScreen", CvScreenEnums.WB_TECH)
				iMaxRows = (screen.getYResolution() - self.iTable_Y - 42) / 24
				nColumns = max(1, min(5, (len(lTech) + iMaxRows - 1)/iMaxRows))
				iWidth = screen.getXResolution() - 40
				iHeight = iMaxRows * 24 + 2
				screen.addTableControlGFC("WBTech", nColumns, 20, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				for i in xrange(nColumns):
						screen.setTableColumnHeader("WBTech", i, "", iWidth/nColumns)

				nRows = (len(lTech) + nColumns - 1) / nColumns
				for i in xrange(nRows):
						screen.appendTableRow("WBTech")

				for iCount in xrange(len(lTech)):
						item = lTech[iCount]
						iRow = iCount % nRows
						iColumn = iCount / nRows
						sItem = item[0]
						ItemInfo = gc.getTechInfo(item[1])
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if ItemInfo.isRepeat():
								if pTeam.getTechCount(item[1]):
										sItem += " (" + str(pTeam.getTechCount(item[1])) + ")"
										sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						elif pTeam.isHasTech(item[1]):
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						screen.setTableText("WBTech", iColumn, iRow, "<font=3>" + sColor + sItem + "</font></color>", ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7871, item[1], CvUtil.FONT_LEFT_JUSTIFY)

		# Updated for PAE (pie)
		def placeTechs(self):
				screen = CyGInterfaceScreen("WBTechScreen", CvScreenEnums.WB_TECH)
				iMaxRows = (screen.getYResolution() - self.iTable_Y - 42) / 24
				nColumns = max(1, min(5, (len(lTech) + iMaxRows - 1)/iMaxRows))
				iWidth = screen.getXResolution() - 40
				iHeight = iMaxRows * 24 + 2
				screen.addTableControlGFC("WBTech", nColumns*2, 20, self.iTable_Y, iWidth, iHeight, False, False, 24, 24, TableStyles.TABLE_STYLE_STANDARD)
				c1 = 0
				c2 = 1
				for i in xrange(nColumns):
						screen.setTableColumnHeader("WBTech", c1, "", iWidth/nColumns-32)
						screen.setTableColumnHeader("WBTech", c2, "", 30)
						c1 = c1 + 2
						c2 = c2 + 2

				nRows = (len(lTech) + nColumns - 1) / nColumns
				for i in xrange(nRows):
						screen.appendTableRow("WBTech")

				for iCount in xrange(len(lTech)):
						item = lTech[iCount]
						iRow = iCount % nRows
						iColumn = iCount / nRows * 2
						sItem = item[0]
						ItemInfo = gc.getTechInfo(item[1])
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if ItemInfo.isRepeat():
								if pTeam.getTechCount(item[1]):
										sItem += " (" + str(pTeam.getTechCount(item[1])) + ")"
										sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						elif pTeam.isHasTech(item[1]):
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						screen.setTableText("WBTech", iColumn, iRow, "<font=3>" + sColor + sItem + "</font></color>", ItemInfo.getButton(), WidgetTypes.WIDGET_PYTHON, 7871, item[1], CvUtil.FONT_LEFT_JUSTIFY)

						# PAE (show info, if Tech cannot be researched (team too))
						button = ""
						iTech = -1
						if gc.getTechInfo(item[1]).getResearchCost() == -1 or not gc.getPlayer(pTeam.getLeaderID()).canEverResearch(item[1]):
								button = gc.getTechInfo(gc.getInfoTypeForString("TECH_NONE")).getButton()

								# Sonderfall zB Griechen: Griechische Tech
								if gc.getPlayer(pTeam.getLeaderID()).canEverResearch(item[1]):
										button = ""
										if not pTeam.isHasTech(item[1]):
												button = "Art/Interface/PlotPicker/Warning.dds"

						else:
								for j in range(gc.getNUM_AND_TECH_PREREQS()):
										eTech = gc.getTechInfo(item[1]).getPrereqAndTechs(j)
										if (eTech > -1):
												if gc.getTechInfo(eTech).getResearchCost() == -1:
														iTech = eTech
														button = gc.getTechInfo(eTech).getButton()
														break

						screen.setTableText("WBTech", iColumn+1, iRow, "", button, WidgetTypes.WIDGET_PYTHON, 7871, iTech, CvUtil.FONT_RIGHT_JUSTIFY)

		def handleInput(self, inputClass):
				screen = CyGInterfaceScreen("WBTechScreen", CvScreenEnums.WB_TECH)
				global iChangeType
				global bApplyAll
				global bNoBarb
				global iSelectedEra

				if inputClass.getFunctionName() == "TechEra":
						iSelectedEra = inputClass.getData() - 1
						self.createTechList()
						self.placeTechs()

				elif inputClass.getFunctionName() == "CurrentTeam":
						iIndex = screen.getPullDownData("CurrentTeam", screen.getSelectedPullDownID("CurrentTeam"))
						self.interfaceScreen(iIndex)

				elif inputClass.getFunctionName() == "ChangeType":
						iChangeType = screen.getPullDownData("ChangeType", screen.getSelectedPullDownID("ChangeType"))

				elif inputClass.getFunctionName() == "CurrentPage":
						iIndex = screen.getPullDownData("CurrentPage", screen.getSelectedPullDownID("CurrentPage"))
						if iIndex == 0:
								WBPlayerScreen.WBPlayerScreen().interfaceScreen(pTeam.getLeaderID())
						elif iIndex == 1:
								WBTeamScreen.WBTeamScreen().interfaceScreen(iTeam)
						elif iIndex == 2:
								WBProjectScreen.WBProjectScreen().interfaceScreen(iTeam)
						elif iIndex == 4:
								WBPlayerUnits.WBPlayerUnits().interfaceScreen(pTeam.getLeaderID())
						elif iIndex == 11:
								WBInfoScreen.WBInfoScreen().interfaceScreen(pTeam.getLeaderID())

				elif inputClass.getFunctionName() == "TechAll":
						for item in lTech:
								ItemInfo = gc.getTechInfo(item[1])
								if ItemInfo.isRepeat():
										continue
								self.editTech(item[1])
						self.placeTechs()

				elif inputClass.getFunctionName() == "WBTech":
						self.editTech(inputClass.getData2())
						self.placeTechs()

				elif inputClass.getFunctionName() == "ApplyAll":
						bApplyAll = not bApplyAll
						sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_WB_COPY_ALL", (CyTranslator().getText("TXT_KEY_MAIN_MENU_PLAYERS", ()),)) + "</font>"
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if bApplyAll:
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						screen.modifyString("ApplyAll", sColor + sText + "</color>", 0)

				elif inputClass.getFunctionName() == "NoBarbarians":
						bNoBarb = not bNoBarb
						sText = u"<font=3b>" + CyTranslator().getText("TXT_KEY_GAME_OPTION_NO_BARBARIANS", ()) + "</font>"
						sColor = CyTranslator().getText("[COLOR_WARNING_TEXT]", ())
						if bNoBarb:
								sColor = CyTranslator().getText("[COLOR_POSITIVE_TEXT]", ())
						screen.modifyString("NoBarbarians", sColor + sText + "</color>", 0)
				return 1

		def editTech(self, item):
				iType = iChangeType
				if bApplyAll:
						for i in xrange(gc.getMAX_TEAMS()):
								pTeamX = gc.getTeam(i)
								if pTeamX.isBarbarian() and bNoBarb:
										continue
								if pTeamX.isAlive():
										if iChangeType == 2:
												iType = not pTeamX.isHasTech(item)
										pTeamX.setHasTech(item, iType, pTeam.getLeaderID(), False, False)
				else:
						if iChangeType == 2:
								iType = not pTeam.isHasTech(item)
						pTeam.setHasTech(item, iType, pTeam.getLeaderID(), False, False)

		def createTechList(self):
				global lTech
				lTech = []
				for i in xrange(gc.getNumTechInfos()):
						ItemInfo = gc.getTechInfo(i)
						if iSelectedEra == -1 or iSelectedEra == ItemInfo.getEra():
								lTech.append([ItemInfo.getDescription(), i])
				# PAE: do not sort (it's better to know the correct time line of techs)
				#lTech.sort()

		def handlePlatyTechAll(self, bEnable):
				for item in lTech:
						ItemInfo = gc.getTechInfo(item[1])
						if ItemInfo.isRepeat():
								continue
						pTeam.setHasTech(item[1], not bEnable, pTeam.getLeaderID(), False, False)

		def update(self, fDelta):
				return 1
