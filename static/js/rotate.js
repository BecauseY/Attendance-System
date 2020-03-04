new function(){
	var rotate = CE.rotate = function(el,time_left,time_right,time_rotate,deg){
		this.el = el;
		this.time_left = time_left = CE.getByClass(el,'div',time_left)[0];
		this.time_right = time_right = CE.getByClass(el,'div',time_right)[0];
		this.time_rotate = time_rotate = CE.getByClass(el,'div',time_rotate)[0];
		this.deg = deg||0;
		this.init();
	};


	rotate.prototype = {
		init:function(){
			if(this.deg >= 0&&this.deg < 180){
				this.time_left.style['z-index'] = '101';
				this.time_right.style.display = 'none';
			}else if(this.deg >= 180){
				this.time_left.style['z-index'] = '99';
				this.time_right.style.display = 'block';
			}
			this.time_rotate.style['transform'] = 'rotate('+this.deg+'deg)';
		},
		setDeg:function(deg){
			this.deg = deg;
			this.init();
		}
	}
}

CE.ready(function(){
	var time_hour = document.getElementById('time-hour');
	var time_minute = document.getElementById('time-minute');
	var time_sec = document.getElementById('time-sec');

	var rotate_hour = new CE.rotate(time_hour,'left','right','rotate');
	var rotate_minute = new CE.rotate(time_minute,'left','right','rotate');
	var rotate_sec = new CE.rotate(time_sec,'left','right','rotate');

	var loop = setInterval(function(){
		var date = new Date();

		var hourText = CE.getByClass(time_hour,'span','time-text')[0];
		var minuteText = CE.getByClass(time_minute,'span','time-text')[0];
		var secondsText = CE.getByClass(time_sec,'span','time-text')[0];

		var hour = date.getHours();
		var minute = date.getMinutes();
		var seconds = date.getSeconds();


		hourText.innerHTML = hour;
		minuteText.innerHTML = minute;
		secondsText.innerHTML = seconds;

		hour = (hour-12)*360/24;
		minute = minute*360/60;
		seconds = seconds*360/60;
		rotate_hour.setDeg(hour);
		rotate_minute.setDeg(minute);
		rotate_sec.setDeg(seconds);
	},200);
});