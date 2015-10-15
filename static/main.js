function formatUtcAsLocal(timeStr) {
    return moment(timeStr).format('YYYY-MM-DD HH:MM');
}

$(function(){
    moment.locale('ru_RU');
    var nowMoment = moment();
    $('.broadcast-time').each(function(){
        var $this = $(this),
            fromTime = $this.data('from-time'),
            toTime = $this.data('to-time'),
            fromTimeMoment = moment(fromTime),
            toTimeMoment = moment(toTime);

        if (fromTimeMoment.isValid())
        {
            $this.text(fromTimeMoment.format('YYYY-MM-DD HH:MM'));
            if (nowMoment.isBefore(fromTimeMoment))
            {
                $this.siblings('.broadcast-status').addClass('status-coming').text(' (' + fromTimeMoment.fromNow() + ')');
            }
            else if (
                (toTimeMoment.isValid() && toTimeMoment.isAfter(nowMoment)) ||
                (!toTimeMoment.isValid() && fromTimeMoment.add(moment.duration(2, 'hours')).isAfter(nowMoment)))
            {
                $this.siblings('.broadcast-status').addClass('status-playing').text(' (сейчас в эфире)');
            }
        }
        else
        {
            $this.text(fromTime);
        }
    });
});
