/**
 * Displays the office hours and weekly calendars using
 * FullCalendar with Google Calendars integration.
 **/

// Change event url to null.
var transform = function(event) {
    event.url = null;
    return event;
}

// Add location to event display.
var render = function(event, element, view) {
    element.append($('<div class="fc-location">').html(event.location));
    return element;
}

// Show the current week during the semester and the first week of class otherwise.
function calendarStartDate() {
    if (moment().isBefore(moment(endDate)) && moment().isAfter(moment(startDate))) {
        return moment();
    }
    return startDate;
}

$(document).ready(function() {
    $('#weekly').fullCalendar({
        eventDataTransform: transform,
        eventRender: render,
        defaultView: $(window).width() >= 768 ? 'agendaWeek' : 'agendaDay',
        allDaySlot: true,
        slotEventOverlap: false,
        weekends: false,
        height: "auto",
        minTime: "09:00:00",
        maxTime: "19:00:00",
        defaultDate: calendarStartDate(),
        googleCalendarApiKey: apiKey,
        eventSources: [
          {
            googleCalendarId: ls88CalendarId,
            cache: true,
            color: '#0072c1'
          },
          {
            googleCalendarId: berkeleyCalendarId,
            cache: true,
            color: '#D81B60'
          },
          {
            googleCalendarId: holidayCalendarId,
            cache: true,
            color: '#0B8043'
          },
          {
            googleCalendarId: holiday2CalendarId,
            cache: true,
            color: '#009688'
          }
        ]
    });
});
