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
    if (event.description !== undefined){
      var content =  event.description + "<br />"; // "<p>" + event.description + "</p>";
    } else {
      var content = "";
    }
    content = content + 'Start: ' + event.starts_at + '<br />End: ' + event.ends_at;
    if (event.location !== undefined){
      element.append($('<div class="fc-location">').html(event.location));
      content = content + '<br />' + event.location; // "<p>" + event.location + "</p>";
    }
    $(element).popover({
      html: true,
      trigger: 'hover',
      title: event.title,
      content: content,
      placement: 'top',
      container: '#weekly',
    });
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
            color: '#C5CAE8' //'#B3E1F7'
          },
          {
            googleCalendarId: berkeleyCalendarId,
            cache: true,
            color: '#F3BACF'
          },
          {
            googleCalendarId: holidayCalendarId,
            cache: true,
            color: '#B5D8C6'
          },
          // {
          //   googleCalendarId: holiday2CalendarId,
          //   cache: true,
          //   color: '#009688'
          // }
        ]
    });
});



        // eventRender: function(event, element) {
        //     $(element).tooltip({title: event.title});             
        // },