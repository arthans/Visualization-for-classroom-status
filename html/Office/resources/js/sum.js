///////////////////////////
// MAIN COMPUTE FUNCTION //
///////////////////////////
function sum(date = new Date()) {
    // constants
    var degreesToRadians = 3.1416 / 180.0000;
    var radiansToDegrees = 180.0000 / 3.1416;
    // retrieve input values
    var inputLongitude = 104.07;
    var inputLatitude = 30.67;
    var inputDate = date.getDate();
    var monthNum = date.getMonth() + 1;
    var inputYear = date.getFullYear();
    var timeHours = date.getHours();
    var timeMinutes = date.getMinutes();
    var inputHoursAfterMidnight = timeHours + timeMinutes / 60.0;
    var inputMinutesAfterMidnight = timeHours * 60.0 + timeMinutes;
    var inputTimeZone = 8;
    // calculate Universal Time
    var UT = inputHoursAfterMidnight - inputTimeZone;
    if (monthNum > 2) {
        correctedYear = inputYear;
        correctedMonth = monthNum - 3;
    } else {
        correctedYear = inputYear - 1;
        correctedMonth = monthNum + 9;
    }
    var t = ((UT / 24.0) + inputDate + Math.floor(30.6 * correctedMonth + 0.5) + Math.floor(365.25 * (correctedYear - 1976)) - 8707.5) / 36525.0;
    var G = 357.528 + 35999.05 * t;
    G = NormalizeTo360(G);
    var C = (1.915 * Math.sin(G * degreesToRadians)) + (0.020 * Math.sin(2.0 * G * degreesToRadians));
    var L = 280.460 + (36000.770 * t) + C;
    L = NormalizeTo360(L);
    var alpha = L - 2.466 * Math.sin(2.0 * L * degreesToRadians) + 0.053 * Math.sin(4.0 * L * degreesToRadians);
    var GHA = UT * 15 - 180 - C + L - alpha;
    GHA = NormalizeTo360(GHA);
    var obliquity = 23.4393 - 0.013 * t;
    var declination = Math.atan(Math.tan(obliquity * degreesToRadians) * Math.sin(alpha * degreesToRadians)) * radiansToDegrees;
    var meridian = inputTimeZone * -15;
    var eotAdjustment = (L - C - alpha) / 15.0;
    var clockTimeToLSOTAdjustment = ((inputLongitude - meridian) / 15.0) - eotAdjustment; // in hours
    var solarHourAngle = GHA + inputLongitude;
    solarHourAngle = NormalizeTo180(solarHourAngle);
    var solarMinutesAfterMidnight = inputMinutesAfterMidnight - (clockTimeToLSOTAdjustment * 60.0);
    var hourAngle = (solarMinutesAfterMidnight - 12 * 60) / 4 * -1;
    // altitude angle
    var altitudeAngle = radiansToDegrees * ArcSin(
        (Math.sin(inputLatitude * degreesToRadians) *
            Math.sin(declination * degreesToRadians)) -
        (Math.cos(inputLatitude * degreesToRadians) *
            Math.cos(declination * degreesToRadians) *
            Math.cos((solarHourAngle + 180) * degreesToRadians)));
    // azimuth angle
    var preAzimuthAngle = radiansToDegrees * ArcCos(
        (Math.cos(declination * degreesToRadians) *
            ((Math.cos(inputLatitude * degreesToRadians) *
                    Math.tan(declination * degreesToRadians)) +
                (Math.sin(inputLatitude * degreesToRadians) *
                    Math.cos((solarHourAngle + 180) * degreesToRadians)))) /
        Math.cos(altitudeAngle * degreesToRadians));
    if ((hourAngle > 0) && (hourAngle < 180)) {
        azimuthAngle = (360.0 - preAzimuthAngle) - 180.0;
    } else {
        azimuthAngle = preAzimuthAngle - 180.0;
    }
    return altitudeAngle, azimuthAngle
}

////////////////////////////////////////////////////////////////////////////////////
// OTHER FUNCTIONS
////////////////////////////////////////////////////////////////////////////////////
function ArcSin(theThing) {
    return (Math.asin(theThing));
}

function ArcCos(theThing) {
    return (Math.acos(theThing));
}

function NormalizeTo360(theThing) {
    return (theThing - Math.floor(theThing / 360.0) * 360);
}

function NormalizeTo180(theThing) {
    theThing = NormalizeTo360(theThing);
    if (theThing > 180) {
        theThing = theThing - 360;
    }
    return (theThing);
}