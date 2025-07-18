# Sid Meier's Civilization 4
# Copyright Firaxis Games 2005
from CvPythonExtensions import (PanelStyles, CyInterface,
																CyGlobalContext, CyArtFileMgr,
																CyUserProfile, CyTranslator, GraphicOptionTypes,
																WidgetTypes, CyGameTextMgr, NotifyCode,
																FontTypes, ButtonStyles, PopupStates,
																InterfaceDirtyBits)

import PyHelpers
import CvUtil
if not CvUtil.isPitbossHost():
    	from CvPythonExtensions import CyGInterfaceScreen
# import ScreenInput
import CvScreenEnums

PyPlayer = PyHelpers.PyPlayer
PyInfo = PyHelpers.PyInfo

# globals
gc = CyGlobalContext()
ArtFileMgr = CyArtFileMgr()
localText = CyTranslator()

MOVIE_SCREEN_WONDER = 0
MOVIE_SCREEN_RELIGION = 1
MOVIE_SCREEN_PROJECT = 2
# PAE Movies +++++++++++
# Victories: 3
# General dying: 4
# Reconquer: 5


class CvWonderMovieScreen:
		"Wonder Movie Screen"

		def __init__(self):
				self.fDelay = -1.0
				self.fTime = 0.0
				self.bDone = False

		def interfaceScreen(self, iMovieItem, iCityId, iMovieType):
				# iMovieItem is either the WonderID, the ReligionID, or the ProjectID, depending on iMovieType

				if CyUserProfile().getGraphicOption(GraphicOptionTypes.GRAPHICOPTION_NO_MOVIES):
						return

				self.Z_CONTROLS = -2.2

				self.X_SCREEN = 0
				self.Y_SCREEN = 0
				self.W_SCREEN = 1024
				self.H_SCREEN = 768

				self.X_WINDOW = 250
				self.Y_WINDOW = 40
				self.W_WINDOW = 760
				self.H_WINDOW = 590
				self.Y_TITLE = self.Y_WINDOW + 20

				self.iWonderId = iMovieItem

				self.X_EXIT = self.X_WINDOW + self.W_WINDOW/2 - 50
				self.Y_EXIT = self.Y_WINDOW + self.H_WINDOW - 50
				self.W_EXIT = 120
				self.H_EXIT = 30

				self.X_MOVIE = 20
				self.Y_MOVIE = 50
				self.W_MOVIE = 720
				self.H_MOVIE = 480

				self.iMovieType = iMovieType
				self.fTime = 0.0
				self.fDelay = 1.5
				self.bDone = False

				# not all projects have movies
				self.szMovieFile = None
				if self.iMovieType == MOVIE_SCREEN_PROJECT:
						szArtDef = gc.getProjectInfo(iMovieItem).getMovieArtDef()
						if (len(szArtDef) > 0):
								self.szMovieFile = CyArtFileMgr().getMovieArtInfo(szArtDef).getPath()
				elif self.iMovieType == MOVIE_SCREEN_WONDER:
						self.szMovieFile = gc.getBuildingInfo(iMovieItem).getMovie()
				elif self.iMovieType == MOVIE_SCREEN_RELIGION:
						self.szMovieFile = gc.getReligionInfo(iMovieItem).getMovieFile()

				# PAE Movies (victories)
				elif self.iMovieType == 3:

						if iMovieItem == 1:
								self.szMovieFile = ArtFileMgr.getMovieArtInfo("ART_DEF_VICTORY_ROME").getPath()
								szHeader = localText.getText("TXT_KEY_POPUP_VICTORY", ())
						elif iMovieItem == 2:
								self.szMovieFile = ArtFileMgr.getMovieArtInfo("ART_DEF_VICTORY_CARTHAGE").getPath()
								szHeader = localText.getText("TXT_KEY_POPUP_VICTORY", ())

				# PAE Movies (general dying)
				elif self.iMovieType == 4:
						self.szMovieFile = "Art/Movies/DyingGeneral/dies"+str(iMovieItem)+".bik"
						szHeader = localText.getText("TXT_KEY_POPUP_GENERAL_DIES", ())

				# PAE Movies (reconquer cities)
				elif self.iMovieType == 5:
						self.szMovieFile = "Art/Movies/Reconquer/triumph"+str(iMovieItem)+".bik"
						szHeader = localText.getText("TXT_KEY_POPUP_RECONQUER", ())

				# -----------------------

				if (self.szMovieFile == None or len(self.szMovieFile) == 0):
						return

				# player = PyPlayer(CyGame().getActivePlayer())

				# move the camera and mark the interface camera as dirty so that it gets reset - JW
				if self.iMovieType == MOVIE_SCREEN_WONDER:
						CyInterface().lookAtCityBuilding(iCityId, iMovieItem)
				# PAE changed from else: only
				elif iCityId > -1:
						CyInterface().lookAtCityBuilding(iCityId, -1)
				CyInterface().setDirty(InterfaceDirtyBits.SelectionCamera_DIRTY_BIT, True)

				screen = CyGInterfaceScreen("WonderMovieScreen" + str(iMovieItem), CvScreenEnums.WONDER_MOVIE_SCREEN)
				screen.addPanel("WonderMoviePanel", "", "", True, True,
												self.X_WINDOW, self.Y_WINDOW, self.W_WINDOW, self.H_WINDOW, PanelStyles.PANEL_STYLE_MAIN)

				screen.showWindowBackground(True)
				screen.setDimensions(screen.centerX(self.X_SCREEN), screen.centerY(self.Y_SCREEN), self.W_SCREEN, self.H_SCREEN)
				screen.setRenderInterfaceOnly(False)
				screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, False)
				screen.enableWorldSounds(False)

				# Header...
				szHeaderId = "WonderTitleHeader" + str(iMovieItem)
				if self.iMovieType == MOVIE_SCREEN_RELIGION:
						szHeader = localText.getText("TXT_KEY_MISC_REL_FOUNDED_MOVIE", (gc.getReligionInfo(iMovieItem).getTextKey(), ))
				elif self.iMovieType == MOVIE_SCREEN_WONDER:
						szHeader = gc.getBuildingInfo(iMovieItem).getDescription()
				elif self.iMovieType == MOVIE_SCREEN_PROJECT:
						szHeader = gc.getProjectInfo(iMovieItem).getDescription()

				screen.setLabel(szHeaderId, "Background", u"<font=4b>" + szHeader + "</font>", CvUtil.FONT_CENTER_JUSTIFY,
												self.X_WINDOW + self.W_WINDOW / 2, self.Y_TITLE, self.Z_CONTROLS, FontTypes.TITLE_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)

				screen.hide("Background")

				screen.playMovie("", 0, 0, 0, 0, 0)  # dummy call to hide screen if no movies are supposed to be shown

		def playMovie(self):

				screen = CyGInterfaceScreen("WonderMovieScreen" + str(self.iWonderId), CvScreenEnums.WONDER_MOVIE_SCREEN)
				screen.setRenderInterfaceOnly(True)
				screen.show("Background")

				# Play the movie
				if self.iMovieType == MOVIE_SCREEN_RELIGION:
						screen.addReligionMovieWidgetGFC("ReligionMovie", self.szMovieFile, self.X_WINDOW + self.X_MOVIE, self.Y_WINDOW +
																						 self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, WidgetTypes.WIDGET_GENERAL, -1, -1)
						CyInterface().playGeneralSound(gc.getReligionInfo(self.iWonderId).getMovieSound())
				else:
						screen.playMovie(self.szMovieFile, self.X_WINDOW + self.X_MOVIE, self.Y_WINDOW + self.Y_MOVIE, self.W_MOVIE, self.H_MOVIE, -2.3)

				screen.setButtonGFC("WonderExit" + str(self.iWonderId), localText.getText("TXT_KEY_MAIN_MENU_OK", ()), "", self.X_EXIT, self.Y_EXIT,
														self.W_EXIT, self.H_EXIT, WidgetTypes.WIDGET_CLOSE_SCREEN, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		# Will handle the input for this screen...
		def handleInput(self, inputClass):
				if (inputClass.getNotifyCode() == NotifyCode.NOTIFY_MOVIE_DONE):
						if (not self.bDone):
								screen = CyGInterfaceScreen("WonderMovieScreen" + str(self.iWonderId), CvScreenEnums.WONDER_MOVIE_SCREEN)
								if self.iMovieType == MOVIE_SCREEN_WONDER:
										szHelp = CyGameTextMgr().getBuildingHelp(self.iWonderId, False, False, False, None)
								elif self.iMovieType == MOVIE_SCREEN_PROJECT:
										szHelp = CyGameTextMgr().getProjectHelp(self.iWonderId, False, None)
								else:
										szHelp = ""

								if len(szHelp) > 0:
										screen.addPanel("MonkeyPanel", "", "", True, True, self.X_WINDOW + self.X_MOVIE + self.W_MOVIE / 8 - 10, self.Y_WINDOW +
																		self.Y_MOVIE + 90, 3 * self.W_MOVIE / 4 + 20, self.H_MOVIE - 180, PanelStyles.PANEL_STYLE_MAIN_BLACK50)
										screen.addMultilineText("MonkeyText", szHelp, self.X_WINDOW + self.X_MOVIE + self.W_MOVIE / 8, self.Y_WINDOW + self.Y_MOVIE + 100,
																						3 * self.W_MOVIE / 4, self.H_MOVIE - 200, WidgetTypes.WIDGET_GENERAL, -1, -1, CvUtil.FONT_LEFT_JUSTIFY)
								self.bDone = True

				return 0

		def update(self, fDelta):

				if self.fDelay > 0:
						self.fTime += fDelta
						if self.fTime > self.fDelay:
								self.playMovie()
								self.fDelay = -1
				return
