#include "CvGameCoreDLL.h"
#include "CyPlayer.h"
#include "CyUnit.h"
#include "CyCity.h"
#include "CyPlot.h"
#include "CySelectionGroup.h"
#include "CyArea.h"
//# include <boost/python/manage_new_object.hpp>
//# include <boost/python/return_value_policy.hpp>
//# include <boost/python/scope.hpp>

//
// published python interface for CyPlayer
//

void CyPlayerPythonInterface1(python::class_<CyPlayer>& x)
{
	OutputDebugString("Python Extension Module - CyPlayerPythonInterface1\n");

	// set the docstring of the current module scope 
	python::scope().attr("__doc__") = "Civilization IV Player Class"; 
	x
		.def("isNone", &CyPlayer::isNone, "checks for a null player")
/********************************************************************************/
/* 	CHANGE_PLAYER							08/27/08			jdog5000	*/
/* 																			*/
/* 	 																		*/
/********************************************************************************/
		.def( "changeLeader", &CyPlayer::changeLeader, "void ( int /*LeaderHeadTypes*/ eNewLeader ) - change leader of player")
		.def( "changeCiv", &CyPlayer::changeCiv, "void ( int /*CivilizationTypes*/ eNewCiv ) - change civilization of player" )
		.def( "setIsHuman", &CyPlayer::setIsHuman, "void ( bool bNewValue ) - set whether player is human" )
/********************************************************************************/
/* 	CHANGE_PLAYER							END								*/
/********************************************************************************/
		.def("startingPlotRange", &CyPlayer::startingPlotRange, "int ()")
		.def("startingPlotWithinRange", &CyPlayer::startingPlotWithinRange, "bool (CyPlot *pPlot, int (PlayerTypes) ePlayer, int iRange, int iPass)")

		.def("findStartingPlot", &CyPlayer::findStartingPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* (bool bRandomize) - Finds a starting plot for player")

		.def("initCity", &CyPlayer::initCity, python::return_value_policy<python::manage_new_object>(), "CyCity* (int x, int y) - spawns a city at x,y")
		.def("acquireCity", &CyPlayer::acquireCity, "void (CyCity* pCity, bool bConquest, bool bTrade)")
		.def("killCities", &CyPlayer::killCities, "void ()")

		.def("getNewCityName", &CyPlayer::getNewCityName, "wstring ()")

		.def("initUnit", &CyPlayer::initUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* (int (UnitTypes) iIndex, int iX, int iY, UnitAITypes eUnitAI, DirectionTypes eFacingDirection) - place Unit at X,Y   NOTE: Always use UnitAITypes.NO_UNITAI")
		.def("disbandUnit", &CyPlayer::disbandUnit, "void (bool bAnnounce)")

		.def("killUnits", &CyPlayer::killUnits, "void ()")
		.def("hasTrait", &CyPlayer::hasTrait, "bool (int (TraitTypes) iIndex) - returns True if player is the Trait Type.")
		.def("isHuman", &CyPlayer::isHuman, "bool ()")
		.def("isBarbarian", &CyPlayer::isBarbarian, "bool () - returns True if player is a Barbarian")
		.def("getName", &CyPlayer::getName, "wstring ()")
		// PBMod
		.def("setName", &CyPlayer::setName, "void (wstring szNewValue) - sets the name to szNewValue")
		// PBMod end
		.def("getNameForm", &CyPlayer::getNameForm, "wstring (int iForm)")
		.def("getNameKey", &CyPlayer::getNameKey, "wstring ()")
		/********************************************************************************/
		/**		REVOLUTION_MOD							1/1/08				jdog5000	*/
		/**																				*/
		/**		For DynamicCivNames														*/
		/********************************************************************************/
		.def("setCivName", &CyPlayer::setCivName, "void(std::wstring szNewDesc, std::wstring szNewShort, std::wstring szNewAdj)" )																														// Exposed to Python
		/********************************************************************************/
		/**		REVOLUTION_MOD							END								*/
		/********************************************************************************/
		.def("getCivilizationDescription", &CyPlayer::getCivilizationDescription, "wstring (int iForm) - returns the Civilization Description String")
		.def("getCivilizationShortDescription", &CyPlayer::getCivilizationShortDescription, "wstring (int iForm) - returns the short Civilization Description")
		.def("getCivilizationDescriptionKey", &CyPlayer::getCivilizationDescriptionKey, "wstring () - returns the Civilization Description String")
		.def("getCivilizationShortDescriptionKey", &CyPlayer::getCivilizationShortDescriptionKey, "wstring () - returns the short Civilization Description")
		.def("getCivilizationAdjective", &CyPlayer::getCivilizationAdjective, "wstring (int iForm) - returns the Civilization name in adjective form")
		.def("getCivilizationAdjectiveKey", &CyPlayer::getCivilizationAdjectiveKey, "wstring ( ) - returns the Civilization name in adjective form")
		.def("getFlagDecal", &CyPlayer::getFlagDecal, "wstring ( ) - returns the Civilization flag decal")
		.def("isWhiteFlag", &CyPlayer::isWhiteFlag, "bool () - Whether or not this player is using a custom texture flag (set in WBS)")
		.def("getStateReligionName", &CyPlayer::getStateReligionName, "wstring (int iForm) - returns the name of the Civilizations State Religion")
		.def("getBestAttackUnitName", &CyPlayer::getBestAttackUnitName, "wstring (int iForm) - returns the name of the best attack unit")
		.def("getWorstEnemyName", &CyPlayer::getWorstEnemyName, "wstring () - returns the name of the worst enemy")
		.def("getStateReligionKey", &CyPlayer::getStateReligionKey, "wstring ( ) - returns the name of the Civilizations State Religion")
		.def("getBestAttackUnitKey", &CyPlayer::getBestAttackUnitKey, "wstring () - returns the name of the best attack unit")
		.def("getArtStyleType", &CyPlayer::getArtStyleType, "int (ArtStyleTypes) () - Returns the ArtStyleType for this player (e.g. European)")
		.def("getUnitButton", &CyPlayer::getUnitButton, " string (int eUnit) - Returns the unit button for this player")

		.def("findBestFoundValue", &CyPlayer::findBestFoundValue, " int () - Finds best found value")

		.def("countNumCoastalCities", &CyPlayer::countNumCoastalCities, "int ()")
		.def("countNumCoastalCitiesByArea", &CyPlayer::countNumCoastalCitiesByArea, "int (CyArea* pArea)")

		.def("countTotalCulture", &CyPlayer::countTotalCulture, "int ()")
		.def("countOwnedBonuses", &CyPlayer::countOwnedBonuses, "int (int (BonusTypes) eBonus) - ")
		.def("countUnimprovedBonuses", &CyPlayer::countUnimprovedBonuses, "int (CyArea* pArea, CyPlot* pFromPlot) - ")
		.def("countCityFeatures", &CyPlayer::countCityFeatures, "int (int (FeatureTypes) eFeature) - Returns ?")
		.def("countNumBuildings", &CyPlayer::countNumBuildings, "int (int (BuildingTypes) eBuilding) - Returns the number of buildings?")
		.def("countPotentialForeignTradeCities", &CyPlayer::countPotentialForeignTradeCities, "int (CyArea* pIgnoreArea) - Returns the number of potential foreign trade cities")
		.def("countPotentialForeignTradeCitiesConnected", &CyPlayer::countPotentialForeignTradeCitiesConnected, "int () - Returns the number of potential foreign trade cities which are also connected to this player's capital")

		.def("canContact", &CyPlayer::canContact, "bool (int (PlayerTypes) ePlayer)")
		.def("contact", &CyPlayer::contact, "void (int (PlayerTypes) ePlayer)")
		.def("canTradeWith", &CyPlayer::canTradeWith, "bool (int (PlayerTypes) eWhoTo)")
		.def("canTradeItem", &CyPlayer::canTradeItem, "bool (int (PlayerTypes) eWhoTo, TradeData item, bool bTestDenial)")
		.def("getTradeDenial", &CyPlayer::getTradeDenial, "DenialTypes (int (PlayerTypes) eWhoTo, TradeData item)")
		.def("canTradeNetworkWith", &CyPlayer::canTradeNetworkWith, "bool (int (PlayerTypes) iPlayer)")
		.def("getNumAvailableBonuses", &CyPlayer::getNumAvailableBonuses, "int (int (BonusTypes) eBonus)")
		.def("getNumTradeableBonuses", &CyPlayer::getNumTradeableBonuses, "int (int (BonusTypes) eBonus)")
		.def("getNumTradeBonusImports", &CyPlayer::getNumTradeBonusImports, "int (int (PlayerTypes) ePlayer)")
		.def("hasBonus", &CyPlayer::hasBonus, "bool (int (BonusTypes) eBonus)")
		.def("canStopTradingWithTeam", &CyPlayer::canStopTradingWithTeam, "bool (int (TeamTypes) eTeam)")
		.def("stopTradingWithTeam", &CyPlayer::stopTradingWithTeam, "void (int (TeamTypes) eTeam)")
		.def("killAllDeals", &CyPlayer::killAllDeals, "void ()")

		.def("findNewCapital", &CyPlayer::findNewCapital, "void ()")
		.def("getNumGovernmentCenters", &CyPlayer::getNumGovernmentCenters, "int ()")
		.def("canRaze", &CyPlayer::canRaze, "bool (CyCity* pCity)")
		.def("raze", &CyPlayer::raze, "void (CyCity* pCity)")
		.def("disband", &CyPlayer::disband, "void (bool bAnnounce)")
		.def("canReceiveGoody", &CyPlayer::canReceiveGoody, "bool (CyPlot* pPlot, int (GoodyTypes) iIndex, CyUnit* pUnit)")
		.def("receiveGoody", &CyPlayer::receiveGoody, "void (CyPlot* pPlot, int (GoodyTypes) iIndex, CyUnit* pUnit)")
		.def("doGoody", &CyPlayer::doGoody, "void (CyPlot* pPlot, CyUnit* pUnit)")
		.def("canFound", &CyPlayer::canFound, "bool (int iX, int iY)")
		.def("found", &CyPlayer::found, "void (int x, int y)")
		.def("canTrain", &CyPlayer::canTrain, "bool (int (UnitTypes) eUnit, bool bContinue, bool bTestVisible)")
		.def("canConstruct", &CyPlayer::canConstruct, "bool (int (BuildingTypes*/eBuilding, bool bContinue, bool bTestVisible, bool bIgnoreCost)")
		.def("canCreate", &CyPlayer::canCreate, "bool (int (ProjectTypes) eProject, bool bContinue, bool bTestVisible)")
		.def("canMaintain", &CyPlayer::canMaintain, "bool (int (ProcessTypes) eProcess, bool bContinue)")
		.def("isProductionMaxedUnitClass", &CyPlayer::isProductionMaxedUnitClass, "bool (int (UnitClassTypes) eUnitClass)")
		.def("isProductionMaxedBuildingClass", &CyPlayer::isProductionMaxedBuildingClass, "bool (int (BuildingClassTypes) eBuildingClass, bool bAcquireCity)")
		.def("isProductionMaxedProject", &CyPlayer::isProductionMaxedProject, "bool (int (ProjectTypes) eProject)")
		.def("getUnitProductionNeeded", &CyPlayer::getUnitProductionNeeded, "int (int (UnitTypes) iIndex)")
		.def("getBuildingProductionNeeded", &CyPlayer::getBuildingProductionNeeded, "int (int (BuildingTypes) iIndex)")
		.def("getProjectProductionNeeded", &CyPlayer::getProjectProductionNeeded, "int (int (ProjectTypes) iIndex)")
		.def("getBuildingClassPrereqBuilding", &CyPlayer::getBuildingClassPrereqBuilding, "int (int (BuildingTypes) eBuilding, int (BuildingClassTypes) ePrereqBuildingClass, int iExtra)")

		.def("removeBuildingClass", &CyPlayer::removeBuildingClass, "void (int (BuildingClassTypes) eBuildingClass)")
		.def("canBuild", &CyPlayer::canBuild, "bool (CyPlot* pPlot, int (BuildTypes) eBuild, bool bTestEra, bool bTestVisible)")

		.def("calculateTotalYield", &CyPlayer::calculateTotalYield, "int (int (YieldTypes) eYield) - Returns the total sum of all city yield")
		.def("calculateTotalExports", &CyPlayer::calculateTotalExports, "int (int (YieldTypes) eYield) - Returns the total sum of all city gold generated for other civs via trade routes")
		.def("calculateTotalImports", &CyPlayer::calculateTotalImports, "int (int (YieldTypes) eYield) - Returns the total sum of all city gold generated for this civ via trade routes with others")

		.def("calculateTotalCityHappiness", &CyPlayer::calculateTotalCityHappiness, "int () - Returns the total sum of all city Happiness values")
		.def("calculateTotalCityUnhappiness", &CyPlayer::calculateTotalCityUnhappiness, "int () - Returns the total sum of all city Unhappiness values")

		.def("calculateTotalCityHealthiness", &CyPlayer::calculateTotalCityHealthiness, "int () - Returns the total sum of all city Healthiness values")
		.def("calculateTotalCityUnhealthiness", &CyPlayer::calculateTotalCityUnhealthiness, "int () - Returns the total sum of all city Unhealthiness values")

		.def("calculateUnitCost", &CyPlayer::calculateUnitCost, "int ()")
		.def("calculateUnitSupply", &CyPlayer::calculateUnitSupply, "int ()")
		.def("calculatePreInflatedCosts", &CyPlayer::calculatePreInflatedCosts, "int ()")
		.def("calculateInflationRate", &CyPlayer::calculateInflationRate, "int ()")
		.def("calculateInflatedCosts", &CyPlayer::calculateInflatedCosts, "int ()")
		.def("calculateGoldRate", &CyPlayer::calculateGoldRate, "int ()")
		.def("calculateTotalCommerce", &CyPlayer::calculateTotalCommerce, "int ()")
		.def("calculateResearchRate", &CyPlayer::calculateResearchRate, "int (int (TechTypes) eTech)")
		.def("calculateBaseNetResearch", &CyPlayer::calculateBaseNetResearch, "int ()")
		.def("calculateResearchModifier", &CyPlayer::calculateResearchModifier, "int (int (TechTypes) eTech)")
		.def("isResearch", &CyPlayer::isResearch, "bool ()")
		.def("canEverResearch", &CyPlayer::canEverResearch, "bool (int (TechTypes) eTech)")
		.def("canResearch", &CyPlayer::canResearch, "bool (int (TechTypes) eTech, bool bTrade)")
		.def("getCurrentResearch", &CyPlayer::getCurrentResearch, "int (TechTypes) ()")
		.def("isCurrentResearchRepeat", &CyPlayer::isCurrentResearchRepeat, "bool ()")
		.def("isNoResearchAvailable", &CyPlayer::isNoResearchAvailable, "bool ()")
		.def("getResearchTurnsLeft", &CyPlayer::getResearchTurnsLeft, "int (int (TechTypes) eTech, bool bOverflow)")

		.def("isCivic", &CyPlayer::isCivic, "bool (int (CivicTypes) eCivic)")
		.def("canDoCivics", &CyPlayer::canDoCivics, "bool (int (CivicTypes) eCivic)")
		.def("canRevolution", &CyPlayer::canRevolution, "bool (int (CivicTypes*) paeNewCivics)")
		.def("revolution", &CyPlayer::revolution, "void (int (CivicTypes*) paeNewCivics, bool bForce)")
		.def("getCivicPercentAnger", &CyPlayer::getCivicPercentAnger, "int (int (CivicTypes) eCivic)")

		.def("canDoReligion", &CyPlayer::canDoReligion, "bool (int (ReligionTypes) eReligion)")
		.def("canChangeReligion", &CyPlayer::canChangeReligion, "bool ()")
		.def("canConvert", &CyPlayer::canConvert, "bool (int (ReligionTypes) iIndex)")
		.def("convert", &CyPlayer::convert, "void (int (ReligionTypes) iIndex)")
		.def("hasHolyCity", &CyPlayer::hasHolyCity, "bool (int (ReligionTypes) eReligion)")
		.def("countHolyCities", &CyPlayer::countHolyCities, "int () - Counts the # of holy cities this player has")

		.def("foundReligion", &CyPlayer::foundReligion, "void (int (ReligionTypes) iIndex, int (ReligionTypes) iSlotReligion, bool bAward)")

		.def("hasHeadquarters", &CyPlayer::hasHeadquarters, "bool (int (CorporationTypes) eCorporation)")
		.def("countHeadquarters", &CyPlayer::countHeadquarters, "int () - Counts the # of headquarters this player has")
		.def("countCorporations", &CyPlayer::countCorporations, "int (int (CorporationTypes) eCorporation) - Counts the # of corporations this player has")
		.def("foundCorporation", &CyPlayer::foundCorporation, "void (int (CorporationTypes) iIndex)")

		.def("getCivicAnarchyLength", &CyPlayer::getCivicAnarchyLength, "int (list (CivicTypes*) paeNewCivics)")
		.def("getReligionAnarchyLength", &CyPlayer::getReligionAnarchyLength, "int ()")

		.def("unitsRequiredForGoldenAge", &CyPlayer::unitsRequiredForGoldenAge, "int ()")
		.def("unitsGoldenAgeCapable", &CyPlayer::unitsGoldenAgeCapable, "int ()")
		.def("unitsGoldenAgeReady", &CyPlayer::unitsGoldenAgeReady, "int ()")
		.def("greatPeopleThreshold", &CyPlayer::greatPeopleThreshold, "int (bool bMilitary)")
		.def("specialistYield", &CyPlayer::specialistYield, "int (int (SpecialistTypes) eSpecialist, int (YieldTypes) eCommerce)")
		.def("specialistCommerce", &CyPlayer::specialistCommerce, "int (int (SpecialistTypes) eSpecialist, int (CommerceTypes) eCommerce)")

		.def("getStartingPlot", &CyPlayer::getStartingPlot, python::return_value_policy<python::manage_new_object>(), "CyPlot* ()")
		.def("setStartingPlot", &CyPlayer::setStartingPlot, "void (CyPlot* pPlot, bool bUpdateStartDist) - sets the player's starting plot")
		.def("getTotalPopulation", &CyPlayer::getTotalPopulation, "int ()")
		.def("getAveragePopulation", &CyPlayer::getAveragePopulation, "int ()")
		.def("getRealPopulation", &CyPlayer::getRealPopulation, "long ()")

		.def("getTotalLand", &CyPlayer::getTotalLand, "int ()")
		.def("getTotalLandScored", &CyPlayer::getTotalLandScored, "int ()")
		.def("getGold", &CyPlayer::getGold, "int ()")
		.def("setGold", &CyPlayer::setGold, "void (int iNewValue)")
		.def("changeGold", &CyPlayer::changeGold, "void (int iChange)")
		.def("getGoldPerTurn", &CyPlayer::getGoldPerTurn, "int ()")

		.def("getAdvancedStartPoints", &CyPlayer::getAdvancedStartPoints, "int ()")
		.def("setAdvancedStartPoints", &CyPlayer::setAdvancedStartPoints, "void (int iNewValue)")
		.def("changeAdvancedStartPoints", &CyPlayer::changeAdvancedStartPoints, "void (int iChange)")
		.def("getAdvancedStartUnitCost", &CyPlayer::getAdvancedStartUnitCost, "int (int (UnitTypes) eUnit, bool bAdd, CyPlot* pPlot)")
		.def("getAdvancedStartCityCost", &CyPlayer::getAdvancedStartCityCost, "int (bool bAdd, CyPlot* pPlot)")
		.def("getAdvancedStartPopCost", &CyPlayer::getAdvancedStartPopCost, "int (bool bAdd, CyCity* pCity)")
		.def("getAdvancedStartCultureCost", &CyPlayer::getAdvancedStartCultureCost, "int (bool bAdd, CyCity* pCity)")
		.def("getAdvancedStartBuildingCost", &CyPlayer::getAdvancedStartBuildingCost, "int (int (BuildingTypes) eBuilding, bool bAdd, CyCity* pCity)")
		.def("getAdvancedStartImprovementCost", &CyPlayer::getAdvancedStartImprovementCost, "int (int (ImprovementTypes) eImprovement, bool bAdd, CyPlot* pPlot)")
		.def("getAdvancedStartRouteCost", &CyPlayer::getAdvancedStartRouteCost, "int (int (RouteTypes) eRoute, bool bAdd, CyPlot* pPlot)")
		.def("getAdvancedStartTechCost", &CyPlayer::getAdvancedStartTechCost, "int (int (TechTypes) eTech, bool bAdd)")
		.def("getAdvancedStartVisibilityCost", &CyPlayer::getAdvancedStartVisibilityCost, "int (bool bAdd, CyPlot* pPlot)")

		.def("getEspionageSpending", &CyPlayer::getEspionageSpending, "int (int (TeamTypes) eIndex)")
		.def("canDoEspionageMission", &CyPlayer::canDoEspionageMission, "bool (int (EspionageMissionTypes) eMission, int (PlayerTypes) eTargetPlayer, CyPlot* pPlot, int iExtraData)")
		.def("getEspionageMissionCost", &CyPlayer::getEspionageMissionCost, "int (int (EspionageMissionTypes) eMission, int (PlayerTypes) eTargetPlayer, CyPlot* pPlot, int iExtraData)")
		.def("doEspionageMission", &CyPlayer::doEspionageMission, "void (int (EspionageMissionTypes) eMission, int (PlayerTypes) eTargetPlayer, CyPlot* pPlot, int iExtraData, CyUnit* pUnit)")
		.def("getEspionageSpendingWeightAgainstTeam", &CyPlayer::getEspionageSpendingWeightAgainstTeam, "int (int (TeamTypes) eIndex)")
		.def("setEspionageSpendingWeightAgainstTeam", &CyPlayer::setEspionageSpendingWeightAgainstTeam, "void (int (TeamTypes) eIndex, int iValue)")
		.def("changeEspionageSpendingWeightAgainstTeam", &CyPlayer::changeEspionageSpendingWeightAgainstTeam, "void (int (TeamTypes) eIndex, int iChange)")

		.def("getGoldenAgeTurns", &CyPlayer::getGoldenAgeTurns, "int ()")
		.def("getGoldenAgeLength", &CyPlayer::getGoldenAgeLength, "int ()")
		.def("isGoldenAge", &CyPlayer::isGoldenAge, "bool ()")
		.def("changeGoldenAgeTurns", &CyPlayer::changeGoldenAgeTurns, "void (int iChange)")
		.def("getNumUnitGoldenAges", &CyPlayer::getNumUnitGoldenAges, "int ()")
		.def("changeNumUnitGoldenAges", &CyPlayer::changeNumUnitGoldenAges, "void (int iChange)")
		.def("getAnarchyTurns", &CyPlayer::getAnarchyTurns, "int ()")
		.def("isAnarchy", &CyPlayer::isAnarchy, "bool ()")
		.def("changeAnarchyTurns", &CyPlayer::changeAnarchyTurns, "void (int iChange)")
		.def("getStrikeTurns", &CyPlayer::getStrikeTurns, "int ()")
		.def("getMaxAnarchyTurns", &CyPlayer::getMaxAnarchyTurns, "int ()")
		.def("getAnarchyModifier", &CyPlayer::getAnarchyModifier, "int ()")
		.def("getGoldenAgeModifier", &CyPlayer::getGoldenAgeModifier, "int ()")
		.def("getHurryModifier", &CyPlayer::getHurryModifier, "int ()")
		.def("createGreatPeople", &CyPlayer::createGreatPeople, "void (int eGreatPersonUnit, bool bIncrementThreshold, bool bIncrementExperience, int iX, int iY)")
		.def("getGreatPeopleCreated", &CyPlayer::getGreatPeopleCreated, "int ()")
		.def("getGreatGeneralsCreated", &CyPlayer::getGreatGeneralsCreated, "int ()")
		.def("getGreatPeopleThresholdModifier", &CyPlayer::getGreatPeopleThresholdModifier, "int ()")
		.def("getGreatGeneralsThresholdModifier", &CyPlayer::getGreatGeneralsThresholdModifier, "int ()")
		.def("getGreatPeopleRateModifier", &CyPlayer::getGreatPeopleRateModifier, "int ()")
		.def("getGreatGeneralRateModifier", &CyPlayer::getGreatGeneralRateModifier, "int ()")
		.def("getDomesticGreatGeneralRateModifier", &CyPlayer::getDomesticGreatGeneralRateModifier, "int ()")
		.def("getStateReligionGreatPeopleRateModifier", &CyPlayer::getStateReligionGreatPeopleRateModifier, "int ()")

		.def("getMaxGlobalBuildingProductionModifier", &CyPlayer::getMaxGlobalBuildingProductionModifier, "int ()")
		.def("getMaxTeamBuildingProductionModifier", &CyPlayer::getMaxTeamBuildingProductionModifier, "int ()")
		.def("getMaxPlayerBuildingProductionModifier", &CyPlayer::getMaxPlayerBuildingProductionModifier, "int ()")
		.def("getFreeExperience", &CyPlayer::getFreeExperience, "int ()")
		.def("getFeatureProductionModifier", &CyPlayer::getFeatureProductionModifier, "int ()")
		.def("getWorkerSpeedModifier", &CyPlayer::getWorkerSpeedModifier, "int ()")
		.def("getImprovementUpgradeRateModifier", &CyPlayer::getImprovementUpgradeRateModifier, "int ()")
		.def("getMilitaryProductionModifier", &CyPlayer::getMilitaryProductionModifier, "int ()")
		.def("getSpaceProductionModifier", &CyPlayer::getSpaceProductionModifier, "int ()")
		.def("getCityDefenseModifier", &CyPlayer::getCityDefenseModifier, "int ()")
		.def("getNumNukeUnits", &CyPlayer::getNumNukeUnits, "int ()")
		.def("getNumOutsideUnits", &CyPlayer::getNumOutsideUnits, "int ()")
		.def("getBaseFreeUnits", &CyPlayer::getBaseFreeUnits, "int ()")
		.def("getBaseFreeMilitaryUnits", &CyPlayer::getBaseFreeMilitaryUnits, "int ()")

		.def("getFreeUnitsPopulationPercent", &CyPlayer::getFreeUnitsPopulationPercent, "int ()")
		.def("getFreeMilitaryUnitsPopulationPercent", &CyPlayer::getFreeMilitaryUnitsPopulationPercent, "int ()")
		.def("getGoldPerUnit", &CyPlayer::getGoldPerUnit, "int ()")
		.def("getGoldPerMilitaryUnit", &CyPlayer::getGoldPerMilitaryUnit, "int ()")
		.def("getExtraUnitCost", &CyPlayer::getExtraUnitCost, "int ()")
		.def("getNumMilitaryUnits", &CyPlayer::getNumMilitaryUnits, "int ()")
		.def("getHappyPerMilitaryUnit", &CyPlayer::getHappyPerMilitaryUnit, "int ()")
		.def("isMilitaryFoodProduction", &CyPlayer::isMilitaryFoodProduction, "bool ()")
		.def("getHighestUnitLevel", &CyPlayer::getHighestUnitLevel, "int ()")

		.def("getConscriptCount", &CyPlayer::getConscriptCount, "int ()")
		.def("setConscriptCount", &CyPlayer::setConscriptCount, "void (int iNewValue)")
		.def("changeConscriptCount", &CyPlayer::changeConscriptCount, "void (int iChange)")

		.def("getMaxConscript", &CyPlayer::getMaxConscript, "int ()")
		.def("getOverflowResearch", &CyPlayer::getOverflowResearch, "int ()")
		.def("isNoUnhealthyPopulation", &CyPlayer::isNoUnhealthyPopulation, "bool ()")
		.def("getExpInBorderModifier", &CyPlayer::getExpInBorderModifier, "bool ()")
		.def("isBuildingOnlyHealthy", &CyPlayer::isBuildingOnlyHealthy, "bool ()")

		.def("getDistanceMaintenanceModifier", &CyPlayer::getDistanceMaintenanceModifier, "int ()")
		.def("getNumCitiesMaintenanceModifier", &CyPlayer::getNumCitiesMaintenanceModifier, "int ()")
		.def("getCorporationMaintenanceModifier", &CyPlayer::getCorporationMaintenanceModifier, "int ()")
		.def("getTotalMaintenance", &CyPlayer::getTotalMaintenance, "int ()")
		.def("getUpkeepModifier", &CyPlayer::getUpkeepModifier, "int ()")
		.def("getLevelExperienceModifier", &CyPlayer::getLevelExperienceModifier, "int ()")

		.def("getExtraHealth", &CyPlayer::getExtraHealth, "int ()")
		.def("getBuildingGoodHealth", &CyPlayer::getBuildingGoodHealth, "int ()")
		.def("getBuildingBadHealth", &CyPlayer::getBuildingBadHealth, "int ()")

		.def("getExtraHappiness", &CyPlayer::getExtraHappiness, "int ()")
		.def("changeExtraHappiness", &CyPlayer::changeExtraHappiness, "void (int iChange)")

		.def("getBuildingHappiness", &CyPlayer::getBuildingHappiness, "int ()")
		.def("getLargestCityHappiness", &CyPlayer::getLargestCityHappiness, "int ()")
		.def("getWarWearinessPercentAnger", &CyPlayer::getWarWearinessPercentAnger, "int ()")
		.def("getWarWearinessModifier", &CyPlayer::getWarWearinessModifier, "int ()")
		.def("getFreeSpecialist", &CyPlayer::getFreeSpecialist, "int ()")
		.def("isNoForeignTrade", &CyPlayer::isNoForeignTrade, "bool ()")
		.def("isNoCorporations", &CyPlayer::isNoCorporations, "bool ()")
		.def("isNoForeignCorporations", &CyPlayer::isNoForeignCorporations, "bool ()")
		.def("getCoastalTradeRoutes", &CyPlayer::getCoastalTradeRoutes, "int ()")
		.def("changeCoastalTradeRoutes", &CyPlayer::changeCoastalTradeRoutes, "void (int iChange)")
		.def("getTradeRoutes", &CyPlayer::getTradeRoutes, "int ()")
		.def("getConversionTimer", &CyPlayer::getConversionTimer, "int ()")
		.def("getRevolutionTimer", &CyPlayer::getRevolutionTimer, "int ()")
		// PBMod
		.def("changeRevolutionTimer", &CyPlayer::changeRevolutionTimer, "void (int iChange)")
		// PBMod end
		.def("isStateReligion", &CyPlayer::isStateReligion, "bool ()")
		.def("isNoNonStateReligionSpread", &CyPlayer::isNoNonStateReligionSpread, "bool ()")
		.def("getStateReligionHappiness", &CyPlayer::getStateReligionHappiness, "int ()")
		.def("getNonStateReligionHappiness", &CyPlayer::getNonStateReligionHappiness, "int ()")
		.def("getStateReligionUnitProductionModifier", &CyPlayer::getStateReligionUnitProductionModifier, "int ()")
		.def("changeStateReligionUnitProductionModifier", &CyPlayer::changeStateReligionUnitProductionModifier, "void (int iChange)")
		.def("getStateReligionBuildingProductionModifier", &CyPlayer::getStateReligionBuildingProductionModifier, "int ()")
		.def("changeStateReligionBuildingProductionModifier", &CyPlayer::changeStateReligionBuildingProductionModifier, "void (int iChange)")
		.def("getStateReligionFreeExperience", &CyPlayer::getStateReligionFreeExperience, "int ()")
		.def("getCapitalCity", &CyPlayer::getCapitalCity, python::return_value_policy<python::manage_new_object>(), "CyCity* ()")
		.def("getCitiesLost", &CyPlayer::getCitiesLost, "int ()")

		.def("getWinsVsBarbs", &CyPlayer::getWinsVsBarbs, "int ()")

		.def("getAssets", &CyPlayer::getAssets, "int ()")
		.def("changeAssets", &CyPlayer::changeAssets, "void (int iChange)")
		.def("getPower", &CyPlayer::getPower, "int ()")
		.def("getPopScore", &CyPlayer::getPopScore, "int ()")
		.def("getLandScore", &CyPlayer::getLandScore, "int ()")
		.def("getWondersScore", &CyPlayer::getWondersScore, "int ()")
		.def("getTechScore", &CyPlayer::getTechScore, "int ()")
		.def("getTotalTimePlayed", &CyPlayer::getTotalTimePlayed, "int ()")
		.def("isMinorCiv", &CyPlayer::isMinorCiv, "bool ()")
		// PBMod
		.def("isWatchingCiv", &CyPlayer::isWatchingCiv, "bool ()")
		.def("setWatchingCiv", &CyPlayer::setWatchingCiv, "void (bool bNewValue)")
		// PBMod end
		.def("isAlive", &CyPlayer::isAlive, "bool ()")
		.def("isEverAlive", &CyPlayer::isEverAlive, "bool ()")
		.def("isExtendedGame", &CyPlayer::isExtendedGame, "bool ()")
		.def("isFoundedFirstCity", &CyPlayer::isFoundedFirstCity, "bool ()")

		.def("isStrike", &CyPlayer::isStrike, "bool ()")

		.def("getID", &CyPlayer::getID, "int ()")
		.def("getHandicapType", &CyPlayer::getHandicapType, "int (HandicapTypes) ()")
		.def("getCivilizationType", &CyPlayer::getCivilizationType, "int (CivilizationTypes )  ()")
		.def("getLeaderType", &CyPlayer::getLeaderType, "int (LeaderHeadTypes) ()")
		.def("getPersonalityType", &CyPlayer::getPersonalityType, "int (LeaderHeadTypes) ()")
		.def("setPersonalityType", &CyPlayer::setPersonalityType, "void (int (LeaderHeadTypes) eNewValue)")
		.def("getCurrentEra", &CyPlayer::getCurrentEra, "int (ErasTypes) ()")
		.def("setCurrentEra", &CyPlayer::setCurrentEra, "void (int (EraTypes) iNewValue)")
		.def("getStateReligion", &CyPlayer::getStateReligion, "wstring (int iForm)")
		.def("setLastStateReligion", &CyPlayer::setLastStateReligion, "void (int (ReligionTypes) iNewReligion) - Sets the player's state religion to iReligionID")
		.def("getTeam", &CyPlayer::getTeam, "int ()")
		.def("isTurnActive", &CyPlayer::isTurnActive, "bool ()")

		.def("getPlayerColor", &CyPlayer::getPlayerColor, "int (PlayerColorTypes) () - returns the color ID of the player")
		.def("getPlayerTextColorR", &CyPlayer::getPlayerTextColorR, "int ()")
		.def("getPlayerTextColorG", &CyPlayer::getPlayerTextColorG, "int ()")
		.def("getPlayerTextColorB", &CyPlayer::getPlayerTextColorB, "int ()")
		.def("getPlayerTextColorA", &CyPlayer::getPlayerTextColorA, "int ()")
		// PBMod
		.def("setPlayerColor", &CyPlayer::setPlayerColor, "void (int (PlayerColorTypes) eColor) - set the color ID of the player")
		// PBMod end
		.def("getSeaPlotYield", &CyPlayer::getSeaPlotYield, "int (YieldTypes eIndex)")
		.def("getYieldRateModifier", &CyPlayer::getYieldRateModifier, "int (YieldTypes eIndex)")
		.def("getCapitalYieldRateModifier", &CyPlayer::getCapitalYieldRateModifier, "int (YieldTypes eIndex)")
		.def("getExtraYieldThreshold", &CyPlayer::getExtraYieldThreshold, "int (YieldTypes eIndex)")
		.def("getTradeYieldModifier", &CyPlayer::getTradeYieldModifier, "int (YieldTypes eIndex)")
		.def("getFreeCityCommerce", &CyPlayer::getFreeCityCommerce, "int (CommerceTypes eIndex)")
		.def("getCommercePercent", &CyPlayer::getCommercePercent, "int (int (CommerceTypes) eIndex)")
		.def("setCommercePercent", &CyPlayer::setCommercePercent, "void (CommerceTypes eIndex, int iNewValue)")
		.def("changeCommercePercent", &CyPlayer::changeCommercePercent, "void (CommerceTypes eIndex, int iChange)")
		.def("getCommerceRate", &CyPlayer::getCommerceRate, "int (CommerceTypes eIndex)")
		.def("getCommerceRateModifier", &CyPlayer::getCommerceRateModifier, "int (CommerceTypes eIndex)")
		.def("getCapitalCommerceRateModifier", &CyPlayer::getCapitalCommerceRateModifier, "int (CommerceTypes eIndex)")
		.def("getStateReligionBuildingCommerce", &CyPlayer::getStateReligionBuildingCommerce, "int (CommerceTypes eIndex)")
		.def("getSpecialistExtraCommerce", &CyPlayer::getSpecialistExtraCommerce, "int (CommerceTypes eIndex)")
		.def("isCommerceFlexible", &CyPlayer::isCommerceFlexible, "bool (int (CommerceTypes) eIndex)")
		.def("getGoldPerTurnByPlayer", &CyPlayer::getGoldPerTurnByPlayer, "int (int (PlayerTypes) eIndex)")

		.def("isFeatAccomplished", &CyPlayer::isFeatAccomplished, "bool (int (FeatTypes) eIndex)")
		.def("setFeatAccomplished", &CyPlayer::setFeatAccomplished, "void (int (FeatTypes) eIndex, bool bNewValue)")
		.def("isOption", &CyPlayer::isOption, "bool (int (PlayerOptionTypes) eIndex)")
		.def("setOption", &CyPlayer::setOption, "void (int (PlayerOptionTypes) eIndex, bool bNewValue)")
		.def("isLoyalMember", &CyPlayer::isLoyalMember, "bool (int (VoteSourceTypes) eIndex)")
		.def("setLoyalMember", &CyPlayer::setLoyalMember, "void (int (VoteSourceTypes) eIndex, bool bNewValue)")
		.def("getVotes", &CyPlayer::getVotes, "int (int (VoteTypes) eVote, int (VoteSourceTypes) eVoteSource)")
		.def("isFullMember", &CyPlayer::isFullMember, "bool (int (VoteSourceTypes) eVoteSource)")
		.def("isVotingMember", &CyPlayer::isVotingMember, "bool (int (VoteSourceTypes) eVoteSource)")
		.def("isPlayable", &CyPlayer::isPlayable, "bool ()")
		.def("setPlayable", &CyPlayer::setPlayable, "void (bool bNewValue)")
		.def("getBonusExport", &CyPlayer::getBonusExport, "int (int (BonusTypes) iIndex)")
		.def("getBonusImport", &CyPlayer::getBonusImport, "int (int (BonusTypes) iIndex)")

		.def("getImprovementCount", &CyPlayer::getImprovementCount, "int (int (ImprovementTypes) iIndex)")

		.def("isBuildingFree", &CyPlayer::isBuildingFree, "bool (int (BuildingTypes) iIndex)")
		.def("getExtraBuildingHappiness", &CyPlayer::getExtraBuildingHappiness, "int (int (BuildingTypes) iIndex)")
		.def("getExtraBuildingHealth", &CyPlayer::getExtraBuildingHealth, "int (int (BuildingTypes) iIndex)")
		.def("getFeatureHappiness", &CyPlayer::getFeatureHappiness, "int (int (FeatureTypes) iIndex)")
		.def("getUnitClassCount", &CyPlayer::getUnitClassCount, "int (int (UnitClassTypes) eIndex)")
		.def("isUnitClassMaxedOut", &CyPlayer::isUnitClassMaxedOut, "bool (int (UnitClassTypes) eIndex, int iExtra)")
		.def("getUnitClassMaking", &CyPlayer::getUnitClassMaking, "int (int (UnitClassTypes) eIndex)")
		.def("getUnitClassCountPlusMaking", &CyPlayer::getUnitClassCountPlusMaking, "int (int (UnitClassTypes) eIndex)")

		.def("getBuildingClassCount", &CyPlayer::getBuildingClassCount, "int (int (BuildingClassTypes) iIndex)")
		.def("isBuildingClassMaxedOut", &CyPlayer::isBuildingClassMaxedOut, "bool (int (BuildingClassTypes) iIndex, int iExtra)")
		.def("getBuildingClassMaking", &CyPlayer::getBuildingClassMaking, "int (int (BuildingClassTypes) iIndex)")
		.def("getBuildingClassCountPlusMaking", &CyPlayer::getBuildingClassCountPlusMaking, "int (int (BuildingClassTypes) iIndex)")
		.def("getHurryCount", &CyPlayer::getHurryCount, "int (int (HurryTypes) eIndex)")
		.def("canHurry", &CyPlayer::canHurry, "bool (int (HurryTypes) eIndex)")
		.def("getSpecialBuildingNotRequiredCount", &CyPlayer::getSpecialBuildingNotRequiredCount, "int (int (SpecialBuildingTypes) eIndex)")
		.def("isSpecialBuildingNotRequired", &CyPlayer::isSpecialBuildingNotRequired, "bool (int (SpecialBuildingTypes) eIndex)")

		.def("isHasCivicOption", &CyPlayer::isHasCivicOption, "bool (int (CivicOptionTypes) eIndex)")
		.def("isNoCivicUpkeep", &CyPlayer::isNoCivicUpkeep, "bool (int (CivicOptionTypes) iIndex)")
		.def("getHasReligionCount", &CyPlayer::getHasReligionCount, "int (int (ReligionTypes) iIndex)")
		.def("countTotalHasReligion", &CyPlayer::countTotalHasReligion, "int () - ")
		.def("getHasCorporationCount", &CyPlayer::getHasCorporationCount, "int (int (CorporationTypes) iIndex)")
		.def("countTotalHasCorporation", &CyPlayer::countTotalHasCorporation, "int () - ")
		.def("findHighestHasReligionCount", &CyPlayer::findHighestHasReligionCount, "int () - ")
		.def("getUpkeepCount", &CyPlayer::getUpkeepCount, "int (int (UpkeepTypes) eIndex)")

		.def("isSpecialistValid", &CyPlayer::isSpecialistValid, "bool (int (SpecialistTypes) iIndex)")
		.def("isResearchingTech", &CyPlayer::isResearchingTech, "bool (int (TechTypes) iIndex)")
		.def("getCivics", &CyPlayer::getCivics, "int ( CivicTypes */ (int (CivicOptionTypes) iIndex)")
		.def("getSingleCivicUpkeep", &CyPlayer::getSingleCivicUpkeep, "int (int (CivicTypes) eCivic, bool bIgnoreAnarchy)")
		.def("getCivicUpkeep", &CyPlayer::getCivicUpkeep, "int (list (CivicTypes) paiCivics, bool bIgnoreAnarchy)")
		.def("setCivics", &CyPlayer::setCivics, "void (int (CivicOptionTypes) eIndex, int (CivicTypes) eNewValue) - Used to forcibly set civics with no anarchy")

		.def("getCombatExperience", &CyPlayer::getCombatExperience, "int () - Combat experience used to produce Warlords")
		.def("changeCombatExperience", &CyPlayer::changeCombatExperience, "void (int iChange) - Combat experience used to produce Warlords")
		.def("setCombatExperience", &CyPlayer::setCombatExperience, "void (int iExperience) - Combat experience used to produce Warlords")

		.def("getSpecialistExtraYield", &CyPlayer::getSpecialistExtraYield, "int (int (SpecialistTypes) eIndex1, int (YieldTypes) eIndex2)")

		.def("findPathLength", &CyPlayer::findPathLength, "int (int (TechTypes) eTech, bool bCost)")

		.def("getQueuePosition", &CyPlayer::getQueuePosition, "int (int (TechTypes) eTech )")
		.def("clearResearchQueue", &CyPlayer::clearResearchQueue, "void ()")
		.def("pushResearch", &CyPlayer::pushResearch, "bool (int (TechTypes) iIndex, bool bClear)")
		.def("popResearch", &CyPlayer::popResearch, "void (int (TechTypes) eTech)")
		.def("getLengthResearchQueue", &CyPlayer::getLengthResearchQueue, "int ()")
		.def("addCityName", &CyPlayer::addCityName, "void (wstring szName)")
		.def("getNumCityNames", &CyPlayer::getNumCityNames, "int ()")
		.def("getCityName", &CyPlayer::getCityName, "wstring (int iIndex)")
		.def("firstCity", &CyPlayer::firstCity, "tuple(CyCity, int iterOut) (bool bReverse) - gets the first city")
		.def("nextCity", &CyPlayer::nextCity, "tuple(CyCity, int iterOut) (int iterIn, bool bReverse) - gets the next city")
		.def("getNumCities", &CyPlayer::getNumCities, "int ()")
		.def("getCity", &CyPlayer::getCity, python::return_value_policy<python::manage_new_object>(), "CyCity* (int iID)")
		.def("firstUnit", &CyPlayer::firstUnit, "tuple(CyUnit, int iterOut) (bool bReverse) - gets the first unit")
		.def("nextUnit", &CyPlayer::nextUnit, "tuple(CyUnit, int iterOut) (int iterIn, bool bReverse) - gets the next unit")
		.def("getNumUnits", &CyPlayer::getNumUnits, "int ()")
		.def("getUnit", &CyPlayer::getUnit, python::return_value_policy<python::manage_new_object>(), "CyUnit* (int iID)")
		.def("firstSelectionGroup", &CyPlayer::firstSelectionGroup, "tuple(CySelectionGroup, int iterOut) (bool bReverse) - gets the first selectionGroup")
		.def("nextSelectionGroup", &CyPlayer::nextSelectionGroup, "tuple(CySelectionGroup, int iterOut) (int iterIn, bool bReverse) - gets the next selectionGroup")
		.def("getNumSelectionGroups", &CyPlayer::getNumSelectionGroups, "int ()")
		.def("getSelectionGroup", &CyPlayer::getSelectionGroup, python::return_value_policy<python::manage_new_object>(), "CySelectionGroup* (int iID)")

		.def("trigger", &CyPlayer::trigger, "void (/*EventTriggerTypes*/int eEventTrigger)")
		.def("getEventOccured", &CyPlayer::getEventOccured, python::return_value_policy<python::reference_existing_object>(), "const EventTriggeredData* (int (EventTypes) eEvent)")
		.def("resetEventOccured", &CyPlayer::resetEventOccured, "void (int (EventTypes) eEvent)")
		.def("getEventTriggered", &CyPlayer::getEventTriggered, python::return_value_policy<python::reference_existing_object>(), "EventTriggeredData* (int iID)")
		.def("initTriggeredData", &CyPlayer::initTriggeredData, python::return_value_policy<python::reference_existing_object>(), "EventTriggeredData* (int (EventTriggerTypes) eEventTrigger, bool bFire, int iCityId, int iPlotX, int iPlotY, int (PlayerTypes) eOtherPlayer, int iOtherPlayerCityId, int (ReligionTypes) eReligion, int (CorporationTypes) eCorporation, int iUnitId, int (BuildingTypes) eBuilding)")
		.def("getEventTriggerWeight", &CyPlayer::getEventTriggerWeight, "int (int (EventTriggerTypes) eTrigger)")
		;
}
