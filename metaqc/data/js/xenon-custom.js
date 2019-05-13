/**
 *	Xenon Main
 *
 *	Theme by: www.laborator.co
 **/

var public_vars = public_vars || {};

;(function($, window, undefined){
	
	"use strict";
	
	$(document).ready(function()
	{	
		// Main Vars
		public_vars.$body                 = $("body");
		public_vars.$pageContainer        = public_vars.$body.find(".page-container");
		public_vars.$chat                 = public_vars.$pageContainer.find("#chat");
		public_vars.$sidebarMenu          = public_vars.$pageContainer.find('.sidebar-menu');
		public_vars.$mainMenu             = public_vars.$sidebarMenu.find('.main-menu');
		
		public_vars.$horizontalNavbar     = public_vars.$body.find('.navbar.horizontal-menu');
		public_vars.$horizontalMenu       = public_vars.$horizontalNavbar.find('.navbar-nav');
		
		public_vars.$mainContent          = public_vars.$pageContainer.find('.main-content');
		public_vars.$mainFooter           = public_vars.$body.find('footer.main-footer');
		
		public_vars.$userInfoMenuHor      = public_vars.$body.find('.navbar.horizontal-menu');
		public_vars.$userInfoMenu         = public_vars.$body.find('nav.navbar.user-info-navbar');
		
		public_vars.$settingsPane         = public_vars.$body.find('.settings-pane');
		public_vars.$settingsPaneIn       = public_vars.$settingsPane.find('.settings-pane-inner');
		
		public_vars.wheelPropagation      = true; // used in Main menu (sidebar)
		
		public_vars.$pageLoadingOverlay   = public_vars.$body.find('.page-loading-overlay');
		
		public_vars.defaultColorsPalette = ['#68b828','#7c38bc','#0e62c7','#fcd036','#4fcdfc','#00b19d','#ff6264','#f7aa47'];
		
		
		
		// Page Loading Overlay
		if(public_vars.$pageLoadingOverlay.length)
		{
			$(window).load(function()
			{
				public_vars.$pageLoadingOverlay.addClass('loaded');
			});
		}
		
		window.onerror = function()
		{
			// failsafe remove loading overlay
			public_vars.$pageLoadingOverlay.addClass('loaded');
		}
		
		
		// Setup Sidebar Menu
		setup_sidebar_menu();
		
		
		// Setup Horizontal Menu
		setup_horizontal_menu();
		
		
		// Sticky Footer
		if(public_vars.$mainFooter.hasClass('sticky'))
		{
			stickFooterToBottom();
			$(window).on('xenon.resized', stickFooterToBottom);
		}
		
		
		// Perfect Scrollbar
		if($.isFunction($.fn.perfectScrollbar))
		{
			if(public_vars.$sidebarMenu.hasClass('fixed'))
				ps_init();
				
			$(".ps-scrollbar").each(function(i, el)
			{
				var $el = $(el);
				
				$el.perfectScrollbar({
					wheelPropagation: false
				});
			});
			
			
			// Chat Scrollbar
			var $chat_inner = public_vars.$pageContainer.find('#chat .chat-inner');
			
			if($chat_inner.parent().hasClass('fixed'))
				$chat_inner.css({maxHeight: $(window).height()}).perfectScrollbar();
				
				
			// User info opening dropdown trigger PS update
			$(".user-info-navbar .dropdown:has(.ps-scrollbar)").each(function(i, el)
			{
				var $scrollbar = $(this).find('.ps-scrollbar');
				
				$(this).on('click', '[data-toggle="dropdown"]', function(ev)
				{
					ev.preventDefault();
					
					setTimeout(function()
					{
						$scrollbar.perfectScrollbar('update');
					}, 1);
				});
			});
			
			
			// Scrollable
			$("div.scrollable").each(function(i, el)
			{
				var $this = $(el),
					max_height = parseInt(attrDefault($this, 'max-height', 200), 10);
				
				max_height = max_height < 0 ? 200 : max_height;
				
				$this.css({maxHeight: max_height}).perfectScrollbar({
					wheelPropagation: true
				});
			});
		}
		
		
		// User info search button
		var $uim_search_form = $(".user-info-menu .search-form, .nav.navbar-right .search-form");
		
		$uim_search_form.each(function(i, el)
		{
			var $uim_search_input = $(el).find('.form-control');
			
			$(el).on('click', '.btn', function(ev)
			{	
				if($uim_search_input.val().trim().length == 0)
				{
					jQuery(el).addClass('focused');
					setTimeout(function(){ $uim_search_input.focus(); }, 100);
					return false;
				}
			});
		
			$uim_search_input.on('blur', function()
			{
				jQuery(el).removeClass('focused');
			});
		});
		
		
		
		// Fixed Footer
		if(public_vars.$mainFooter.hasClass('fixed'))
		{
			public_vars.$mainContent.css({
				paddingBottom: public_vars.$mainFooter.outerHeight(true)
			});
		}
		


		// Go to to links
		$('body').on('click', 'a[rel="go-top"]', function(ev)
		{
			ev.preventDefault();

			var obj = {pos: $(window).scrollTop()};

			TweenLite.to(obj, .3, {pos: 0, ease:Power4.easeOut, onUpdate: function()
			{
				$(window).scrollTop(obj.pos);
			}});
		});


		
		
		// User info navbar equal heights
		if(public_vars.$userInfoMenu.length)
		{
			public_vars.$userInfoMenu.find('.user-info-menu > li').css({
				minHeight: public_vars.$userInfoMenu.outerHeight() - 1
			});
		}
		
		
		
		// Autosize
		if($.isFunction($.fn.autosize))
		{
			$(".autosize, .autogrow").autosize();
		}
		
		
		// Custom Checkboxes & radios
		cbr_replace();
		
		
		
		// Auto hidden breadcrumbs
		$(".breadcrumb.auto-hidden").each(function(i, el)
		{
			var $bc = $(el),
				$as = $bc.find('li a'),
				collapsed_width = $as.width(),
				expanded_width = 0;
			
			$as.each(function(i, el)
			{
				var $a = $(el);
				
				expanded_width = $a.outerWidth(true);
				$a.addClass('collapsed').width(expanded_width);
				
				$a.hover(function()
				{
					$a.removeClass('collapsed');
				},
				function()
				{
					$a.addClass('collapsed');
				});
			});
		});
		
		
		
		// Close Modal on Escape Keydown
		$(window).on('keydown', function(ev)
		{
			// Escape
			if(ev.keyCode == 27)
			{
				// Close opened modal
				if(public_vars.$body.hasClass('modal-open'))
					$(".modal-open .modal:visible").modal('hide');
			}
		});
		
		
		// Minimal Addon focus interaction
		$(".input-group.input-group-minimal:has(.form-control)").each(function(i, el)
		{
			var $this = $(el),
				$fc = $this.find('.form-control');
			
			$fc.on('focus', function()
			{
				$this.addClass('focused');
			}).on('blur', function()
			{
				$this.removeClass('focused');
			});
		});
		
		
		
		// Spinner
		$(".input-group.spinner").each(function(i, el)
		{
			var $ig = $(el),
				$dec = $ig.find('[data-type="decrement"]'),
				$inc = $ig.find('[data-type="increment"]'),
				$inp = $ig.find('.form-control'),
				
				step = attrDefault($ig, 'step', 1),
				min = attrDefault($ig, 'min', 0),
				max = attrDefault($ig, 'max', 0),
				umm = min < max;
				
			
			$dec.on('click', function(ev)
			{
				ev.preventDefault();

				var num = new Number($inp.val()) - step;
				
				if(umm && num <= min)
				{
					num = min;
				}
				
				$inp.val(num);
			});
			
			$inc.on('click', function(ev)
			{
				ev.preventDefault();

				var num = new Number($inp.val()) + step;
				
				if(umm && num >= max)
				{
					num = max;
				}
				
				$inp.val(num);
			});
		});
		
		
		
		
		// Select2 Dropdown replacement
		if($.isFunction($.fn.select2))
		{
			$(".select2").each(function(i, el)
			{
				var $this = $(el),
					opts = {
						allowClear: attrDefault($this, 'allowClear', false)
					};
				
				$this.select2(opts);
				$this.addClass('visible');
				
				//$this.select2("open");
			});
			
			
			if($.isFunction($.fn.niceScroll))
			{
				$(".select2-results").niceScroll({
					cursorcolor: '#d4d4d4',
					cursorborder: '1px solid #ccc',
					railpadding: {right: 3}
				});
			}
		}
		
		
		
		
		// SelectBoxIt Dropdown replacement
		if($.isFunction($.fn.selectBoxIt))
		{
			$("select.selectboxit").each(function(i, el)
			{
				var $this = $(el),
					opts = {
						showFirstOption: attrDefault($this, 'first-option', true),
						'native': attrDefault($this, 'native', false),
						defaultText: attrDefault($this, 'text', ''),
					};
					
				$this.addClass('visible');
				$this.selectBoxIt(opts);
			});
		}
		
		
		
		// Datepicker
		if($.isFunction($.fn.datepicker))
		{
			$(".datepicker").each(function(i, el)
			{
				var $this = $(el),
					opts = {
						format: attrDefault($this, 'format', 'mm/dd/yyyy'),
						startDate: attrDefault($this, 'startDate', ''),
						endDate: attrDefault($this, 'endDate', ''),
						daysOfWeekDisabled: attrDefault($this, 'disabledDays', ''),
						startView: attrDefault($this, 'startView', 0),
						rtl: rtl()
					},
					$n = $this.next(),
					$p = $this.prev();
								
				$this.datepicker(opts);
				
				if($n.is('.input-group-addon') && $n.has('a'))
				{
					$n.on('click', function(ev)
					{
						ev.preventDefault();
						
						$this.datepicker('show');
					});
				}
				
				if($p.is('.input-group-addon') && $p.has('a'))
				{
					$p.on('click', function(ev)
					{
						ev.preventDefault();
						
						$this.datepicker('show');
					});
				}
			});
		}
		
		
		
		// Date Range Picker
		if($.isFunction($.fn.daterangepicker))
		{
			$(".daterange").each(function(i, el)
			{
				// Change the range as you desire
				var ranges = {
					'Today': [moment(), moment()],
					'Yesterday': [moment().subtract('days', 1), moment().subtract('days', 1)],
					'Last 7 Days': [moment().subtract('days', 6), moment()],
					'Last 30 Days': [moment().subtract('days', 29), moment()],
					'This Month': [moment().startOf('month'), moment().endOf('month')],
					'Last Month': [moment().subtract('month', 1).startOf('month'), moment().subtract('month', 1).endOf('month')]
				};
				
				var $this = $(el),
					opts = {
						format: attrDefault($this, 'format', 'MM/DD/YYYY'),
						timePicker: attrDefault($this, 'timePicker', false),
						timePickerIncrement: attrDefault($this, 'timePickerIncrement', false),
						separator: attrDefault($this, 'separator', ' - '),
					},
					min_date = attrDefault($this, 'minDate', ''),
					max_date = attrDefault($this, 'maxDate', ''),
					start_date = attrDefault($this, 'startDate', ''),
					end_date = attrDefault($this, 'endDate', '');
				
				if($this.hasClass('add-ranges'))
				{
					opts['ranges'] = ranges;
				}	
					
				if(min_date.length)
				{
					opts['minDate'] = min_date;
				}
					
				if(max_date.length)
				{
					opts['maxDate'] = max_date;
				}
					
				if(start_date.length)
				{
					opts['startDate'] = start_date;
				}
					
				if(end_date.length)
				{
					opts['endDate'] = end_date;
				}
				
				
				$this.daterangepicker(opts, function(start, end)
				{
					var drp = $this.data('daterangepicker');
					
					if($this.is('[data-callback]'))
					{
						//daterange_callback(start, end);
						callback_test(start, end);
					}
					
					if($this.hasClass('daterange-inline'))
					{
						$this.find('span').html(start.format(drp.format) + drp.separator + end.format(drp.format));
					}
				});
				
				if(typeof opts['ranges'] == 'object')
				{
					$this.data('daterangepicker').container.removeClass('show-calendar');
				}
			});
		}
		
		
		
		// Timepicker
		if($.isFunction($.fn.timepicker))
		{
			$(".timepicker").each(function(i, el)
			{
				var $this = $(el),
					opts = {
						template: attrDefault($this, 'template', false),
						showSeconds: attrDefault($this, 'showSeconds', false),
						defaultTime: attrDefault($this, 'defaultTime', 'current'),
						showMeridian: attrDefault($this, 'showMeridian', true),
						minuteStep: attrDefault($this, 'minuteStep', 15),
						secondStep: attrDefault($this, 'secondStep', 15)
					},
					$n = $this.next(),
					$p = $this.prev();
				
				$this.timepicker(opts);
				
				if($n.is('.input-group-addon') && $n.has('a'))
				{
					$n.on('click', function(ev)
					{
						ev.preventDefault();
						
						$this.timepicker('showWidget');
					});
				}
				
				if($p.is('.input-group-addon') && $p.has('a'))
				{
					$p.on('click', function(ev)
					{
						ev.preventDefault();
						
						$this.timepicker('showWidget');
					});
				}
			});
		}
		
		
		
		// Colorpicker
		if($.isFunction($.fn.colorpicker))
		{
			$(".colorpicker").each(function(i, el)
			{
				var $this = $(el),
					opts = {
					},
					$n = $this.next(),
					$p = $this.prev(),
					
					$preview = $this.siblings('.input-group-addon').find('.color-preview');
				
				$this.colorpicker(opts);
				
				if($n.is('.input-group-addon') && $n.has('a'))
				{
					$n.on('click', function(ev)
					{
						ev.preventDefault();
						
						$this.colorpicker('show');
					});
				}
				
				if($p.is('.input-group-addon') && $p.has('a'))
				{
					$p.on('click', function(ev)
					{
						ev.preventDefault();
						
						$this.colorpicker('show');
					});
				}
				
				if($preview.length)
				{
					$this.on('changeColor', function(ev){
						
						$preview.css('background-color', ev.color.toHex());
					});
					
					if($this.val().length)
					{
						$preview.css('background-color', $this.val());
					}
				}
			});
		}
		
		
		
		
		// Form Validation
		if($.isFunction($.fn.validate))
		{
			$("form.validate").each(function(i, el)
			{
				var $this = $(el),
					opts = {
						rules: {},
						messages: {},
						errorElement: 'span',
						errorClass: 'validate-has-error',
						highlight: function (element) {
							$(element).closest('.form-group').addClass('validate-has-error');
						},
						unhighlight: function (element) {
							$(element).closest('.form-group').removeClass('validate-has-error');
						},
						errorPlacement: function (error, element)
						{
							if(element.closest('.has-switch').length)
							{
								error.insertAfter(element.closest('.has-switch'));
							}
							else
							if(element.parent('.checkbox, .radio').length || element.parent('.input-group').length)
							{
								error.insertAfter(element.parent());
							} 
							else 
							{
								error.insertAfter(element);
							}
						}
					},
					$fields = $this.find('[data-validate]');
				
					
				$fields.each(function(j, el2)
				{
					var $field = $(el2),
						name = $field.attr('name'),
						validate = attrDefault($field, 'validate', '').toString(),
						_validate = validate.split(',');
					
					for(var k in _validate)
					{
						var rule = _validate[k],
							params,
							message;
						
						if(typeof opts['rules'][name] == 'undefined')
						{
							opts['rules'][name] = {};
							opts['messages'][name] = {};
						}
						
						if($.inArray(rule, ['required', 'url', 'email', 'number', 'date', 'creditcard']) != -1)
						{
							opts['rules'][name][rule] = true;
							
							message = $field.data('message-' + rule);
							
							if(message)
							{
								opts['messages'][name][rule] = message;
							}
						}
						// Parameter Value (#1 parameter)
						else 
						if(params = rule.match(/(\w+)\[(.*?)\]/i))
						{
							if($.inArray(params[1], ['min', 'max', 'minlength', 'maxlength', 'equalTo']) != -1)
							{
								opts['rules'][name][params[1]] = params[2];
								
							
								message = $field.data('message-' + params[1]);
								
								if(message)
								{
									opts['messages'][name][params[1]] = message;
								}
							}
						}
					}
				});
				
				$this.validate(opts);
			});
		}
		
		
		
		
		// Input Mask
		if($.isFunction($.fn.inputmask))
		{
			$("[data-mask]").each(function(i, el)
			{
				var $this = $(el),
					mask = $this.data('mask').toString(),
					opts = {
						numericInput: attrDefault($this, 'numeric', false),
						radixPoint: attrDefault($this, 'radixPoint', ''),
						rightAlign: attrDefault($this, 'numericAlign', 'left') == 'right'
					},
					placeholder = attrDefault($this, 'placeholder', ''),
					is_regex = attrDefault($this, 'isRegex', '');
					
				if(placeholder.length)
				{
					opts[placeholder] = placeholder;
				}
				
				switch(mask.toLowerCase())
				{
					case "phone":
						mask = "(999) 999-9999";
						break;
						
					case "currency":
					case "rcurrency":
					
						var sign = attrDefault($this, 'sign', '$');;
						
						mask = "999,999,999.99";
						
						if($this.data('mask').toLowerCase() == 'rcurrency')
						{
							mask += ' ' + sign;
						}
						else
						{
							mask = sign + ' ' + mask;
						}
						
						opts.numericInput = true;
						opts.rightAlignNumerics = false;
						opts.radixPoint = '.';
						break;
						
					case "email":
						mask = 'Regex';
						opts.regex = "[a-zA-Z0-9._%-]+@[a-zA-Z0-9-]+\\.[a-zA-Z]{2,4}";
						break;
					
					case "fdecimal":
						mask = 'decimal';
						$.extend(opts, {
							autoGroup		: true,
							groupSize		: 3,
							radixPoint		: attrDefault($this, 'rad', '.'),
							groupSeparator	: attrDefault($this, 'dec', ',')
						});
				}
				
				if(is_regex)
				{
					opts.regex = mask;
					mask = 'Regex';
				}
				
				$this.inputmask(mask, opts);
			});
		}
		
		
		
		// Form Wizard
		if($.isFunction($.fn.bootstrapWizard))
		{
			$(".form-wizard").each(function(i, el)
			{
				var $this = $(el),
					$tabs = $this.find('> .tabs > li'),
					$progress = $this.find(".progress-indicator"),
					_index = $this.find('> ul > li.active').index();
				
				// Validation
				var checkFormWizardValidaion = function(tab, navigation, index)
					{
			  			if($this.hasClass('validate'))
			  			{
							var $valid = $this.valid();
							
							if( ! $valid)
							{
								$this.data('validator').focusInvalid();
								return false;
							}
						}
						
				  		return true;
					};
				
				// Setup Progress
				if(_index > 0)
				{
					$progress.css({width: _index/$tabs.length * 100 + '%'});
					$tabs.removeClass('completed').slice(0, _index).addClass('completed');
				}
				
				$this.bootstrapWizard({
					tabClass: "",
			  		onTabShow: function($tab, $navigation, index)
			  		{
			  			var pct = $tabs.eq(index).position().left / $tabs.parent().width() * 100;
			  			
			  			$tabs.removeClass('completed').slice(0, index).addClass('completed');
			  			$progress.css({width: pct + '%'});
			  		},
			  		
			  		onNext: checkFormWizardValidaion,
			  		onTabClick: checkFormWizardValidaion
			  	});
			  	
			  	$this.data('bootstrapWizard').show( _index );
			  	
			  	$this.find('.pager a').on('click', function(ev)
			  	{
				  	ev.preventDefault();
			  	});
			});
		}
		
		
		
		
		// Slider
		if($.isFunction($.fn.slider))
		{
			$(".slider").each(function(i, el)
			{
				var $this = $(el),
					$label_1 = $('<span class="ui-label"></span>'),
					$label_2 = $label_1.clone(),
					
					orientation = attrDefault($this, 'vertical', 0) != 0 ? 'vertical' : 'horizontal',
					
					prefix = attrDefault($this, 'prefix', ''),
					postfix = attrDefault($this, 'postfix', ''),
					
					fill = attrDefault($this, 'fill', ''),
					$fill = $(fill),
					
					step = attrDefault($this, 'step', 1),
					value = attrDefault($this, 'value', 5),
					min = attrDefault($this, 'min', 0),
					max = attrDefault($this, 'max', 100),
					min_val = attrDefault($this, 'min-val', 10),
					max_val = attrDefault($this, 'max-val', 90),
					
					is_range = $this.is('[data-min-val]') || $this.is('[data-max-val]'),
					
					reps = 0;
				
				
				// Range Slider Options
				if(is_range)
				{
					$this.slider({
						range: true,
						orientation: orientation,
						min: min,
						max: max,
						values: [min_val, max_val],
						step: step,
						slide: function(e, ui)
						{
							var min_val = (prefix ? prefix : '') + ui.values[0] + (postfix ? postfix : ''),
								max_val = (prefix ? prefix : '') + ui.values[1] + (postfix ? postfix : '');
							
							$label_1.html( min_val );
							$label_2.html( max_val );
							
							if(fill)
								$fill.val(min_val + ',' + max_val);
								
							reps++;
						},
						change: function(ev, ui)
						{
							if(reps == 1)
							{
								var min_val = (prefix ? prefix : '') + ui.values[0] + (postfix ? postfix : ''),
									max_val = (prefix ? prefix : '') + ui.values[1] + (postfix ? postfix : '');
								
								$label_1.html( min_val );
								$label_2.html( max_val );
								
								if(fill)
									$fill.val(min_val + ',' + max_val);
							}
							
							reps = 0;
						}
					});
				
					var $handles = $this.find('.ui-slider-handle');
						
					$label_1.html((prefix ? prefix : '') + min_val + (postfix ? postfix : ''));
					$handles.first().append( $label_1 );
					
					$label_2.html((prefix ? prefix : '') + max_val+ (postfix ? postfix : ''));
					$handles.last().append( $label_2 );
				}
				// Normal Slider
				else
				{	
					
					$this.slider({
						range: attrDefault($this, 'basic', 0) ? false : "min",
						orientation: orientation,
						min: min,
						max: max,
						value: value,
						step: step,
						slide: function(ev, ui)
						{
							var val = (prefix ? prefix : '') + ui.value + (postfix ? postfix : '');
							
							$label_1.html( val );
							
							
							if(fill)
								$fill.val(val);
							
							reps++;
						},
						change: function(ev, ui)
						{
							if(reps == 1)
							{
								var val = (prefix ? prefix : '') + ui.value + (postfix ? postfix : '');
								
								$label_1.html( val );
								
								if(fill)
									$fill.val(val);
							}
							
							reps = 0;
						}
					});
					
					var $handles = $this.find('.ui-slider-handle');
						//$fill = $('<div class="ui-fill"></div>');
					
					$label_1.html((prefix ? prefix : '') + value + (postfix ? postfix : ''));
					$handles.html( $label_1 );
					
					//$handles.parent().prepend( $fill );
					
					//$fill.width($handles.get(0).style.left);
				}
				
			})
		}

		
		
		
		// jQuery Knob
		if($.isFunction($.fn.knob))
		{		
			$(".knob").knob({
				change: function (value) {
				},
				release: function (value) {
				},
				cancel: function () {
				},
				draw: function () {
				
					if (this.$.data('skin') == 'tron') {
				
						var a = this.angle(this.cv) // Angle
							,
							sa = this.startAngle // Previous start angle
							,
							sat = this.startAngle // Start angle
							,
							ea // Previous end angle
							, eat = sat + a // End angle
							,
							r = 1;
				
						this.g.lineWidth = this.lineWidth;
				
						this.o.cursor && (sat = eat - 0.3) && (eat = eat + 0.3);
				
						if (this.o.displayPrevious) {
							ea = this.startAngle + this.angle(this.v);
							this.o.cursor && (sa = ea - 0.3) && (ea = ea + 0.3);
							this.g.beginPath();
							this.g.strokeStyle = this.pColor;
							this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, sa, ea, false);
							this.g.stroke();
						}
				
						this.g.beginPath();
						this.g.strokeStyle = r ? this.o.fgColor : this.fgColor;
						this.g.arc(this.xy, this.xy, this.radius - this.lineWidth, sat, eat, false);
						this.g.stroke();
				
						this.g.lineWidth = 2;
						this.g.beginPath();
						this.g.strokeStyle = this.o.fgColor;
						this.g.arc(this.xy, this.xy, this.radius - this.lineWidth + 1 + this.lineWidth * 2 / 3, 0, 2 * Math.PI, false);
						this.g.stroke();
				
						return false;
					}
				}
			});
		}
		
		
		
		
		// Wysiwyg Editor
		if($.isFunction($.fn.wysihtml5))
		{
			$(".wysihtml5").each(function(i, el)
			{
				var $this = $(el),
					stylesheets = attrDefault($this, 'stylesheet-url', '')
				
				$(".wysihtml5").wysihtml5({
					size: 'white',
					stylesheets: stylesheets.split(','),
					"html": attrDefault($this, 'html', true),
					"color": attrDefault($this, 'colors', true),
				});
			});
		}
		
		
		
		
		// CKeditor WYSIWYG
		if($.isFunction($.fn.ckeditor))
		{
			$(".ckeditor").ckeditor({
				contentsLangDirection: rtl() ? 'rtl' : 'ltr'
			});
		}
		
		
		
		// Dropzone is prezent
		if(typeof Dropzone != 'undefined')
		{
			Dropzone.autoDiscover = false;
			
			$(".dropzone[action]").each(function(i, el)
			{
				$(el).dropzone();
			});
		}
		
		
		
		
		// Tocify Table
		if($.isFunction($.fn.tocify) && $("#toc").length)
		{
			$("#toc").tocify({ 
				context: '.tocify-content', 
				selectors: "h2,h3,h4,h5" 
			});
			
			
			var $this = $(".tocify"),
				watcher = scrollMonitor.create($this.get(0));
			
			$this.width( $this.parent().width() );
			
			watcher.lock();

			watcher.stateChange(function() 
			{
				$($this.get(0)).toggleClass('fixed', this.isAboveViewport)
			});
		}
		
		
		
		// Login Form Label Focusing
		$(".login-form .form-group:has(label)").each(function(i, el)
		{
			var $this = $(el),
				$label = $this.find('label'),
				$input = $this.find('.form-control');
			
			$input.on('focus', function()
			{
				$this.addClass('is-focused');
			});
			
			$input.on('keydown', function()
			{
				$this.addClass('is-focused');
			});
				
			$input.on('blur', function()
			{
				$this.removeClass('is-focused');
				
				if($input.val().trim().length > 0)
				{
					$this.addClass('is-focused');
				}
			});
			
			$label.on('click', function()
			{
				$input.focus();
			});
			
			if($input.val().trim().length > 0)
			{
				$this.addClass('is-focused');
			}
		});
		
	});


	// Enable/Disable Resizable Event
	var wid = 0;
	
	$(window).resize(function() {
		clearTimeout(wid);
		wid = setTimeout(trigger_resizable, 200);
	});
	

})(jQuery, window);



// Sideber Menu Setup function
var sm_duration = .2,
	sm_transition_delay = 150;

function setup_sidebar_menu()
{
	if(public_vars.$sidebarMenu.length)
	{
		var $items_with_subs = public_vars.$sidebarMenu.find('li:has(> ul)'),
			toggle_others = public_vars.$sidebarMenu.hasClass('toggle-others');
		
		$items_with_subs.filter('.active').addClass('expanded');
		
		$items_with_subs.each(function(i, el)
		{
			var $li = jQuery(el),
				$a = $li.children('a'),
				$sub = $li.children('ul');
			
			$li.addClass('has-sub');
			
			$a.on('click', function(ev)
			{
				ev.preventDefault();
				
				if(toggle_others)
				{
					sidebar_menu_close_items_siblings($li);
				}
				
				if($li.hasClass('expanded') || $li.hasClass('opened'))
					sidebar_menu_item_collapse($li, $sub);
				else
					sidebar_menu_item_expand($li, $sub);
			});
		});
	}
}

function sidebar_menu_item_expand($li, $sub)
{
	if($li.data('is-busy') || ($li.parent('.main-menu').length && public_vars.$sidebarMenu.hasClass('collapsed')))
		return;
		
	$li.addClass('expanded').data('is-busy', true);
	$sub.show();
	
	var $sub_items 	  = $sub.children(),
		sub_height	= $sub.outerHeight(),
		
		win_y			 = jQuery(window).height(),
		total_height	  = $li.outerHeight(),
		current_y		 = public_vars.$sidebarMenu.scrollTop(),
		item_max_y		= $li.position().top + current_y,
		fit_to_viewpport  = public_vars.$sidebarMenu.hasClass('fit-in-viewport');
		
	$sub_items.addClass('is-hidden');
	$sub.height(0);
	
	
	TweenMax.to($sub, sm_duration, {css: {height: sub_height}, onUpdate: ps_update, onComplete: function(){ 
		$sub.height(''); 
	}});
	
	var interval_1 = $li.data('sub_i_1'),
		interval_2 = $li.data('sub_i_2');
	
	window.clearTimeout(interval_1);
	
	interval_1 = setTimeout(function()
	{
		$sub_items.each(function(i, el)
		{
			var $sub_item = jQuery(el);
			
			$sub_item.addClass('is-shown');
		});
		
		var finish_on = sm_transition_delay * $sub_items.length,
			t_duration = parseFloat($sub_items.eq(0).css('transition-duration')),
			t_delay = parseFloat($sub_items.last().css('transition-delay'));
		
		if(t_duration && t_delay)
		{
			finish_on = (t_duration + t_delay) * 1000;
		}
		
		// In the end
		window.clearTimeout(interval_2);
	
		interval_2 = setTimeout(function()
		{
			$sub_items.removeClass('is-hidden is-shown');
			
		}, finish_on);
	
		
		$li.data('is-busy', false);
		
	}, 0);
	
	$li.data('sub_i_1', interval_1),
	$li.data('sub_i_2', interval_2);
}

function sidebar_menu_item_collapse($li, $sub)
{
	if($li.data('is-busy'))
		return;
	
	var $sub_items = $sub.children();
	
	$li.removeClass('expanded').data('is-busy', true);
	$sub_items.addClass('hidden-item');
	
	TweenMax.to($sub, sm_duration, {css: {height: 0}, onUpdate: ps_update, onComplete: function()
	{
		$li.data('is-busy', false).removeClass('opened');
		
		$sub.attr('style', '').hide();
		$sub_items.removeClass('hidden-item');
		
		$li.find('li.expanded ul').attr('style', '').hide().parent().removeClass('expanded');
		
		ps_update(true);
	}});
}

function sidebar_menu_close_items_siblings($li)
{
	$li.siblings().not($li).filter('.expanded, .opened').each(function(i, el)
	{
		var $_li = jQuery(el),
			$_sub = $_li.children('ul');
		
		sidebar_menu_item_collapse($_li, $_sub);
	});
}


// Horizontal Menu
function setup_horizontal_menu()
{
	if(public_vars.$horizontalMenu.length)
	{
		var $items_with_subs = public_vars.$horizontalMenu.find('li:has(> ul)'),
			click_to_expand = public_vars.$horizontalMenu.hasClass('click-to-expand');
		
		if(click_to_expand)
		{
			public_vars.$mainContent.add( public_vars.$sidebarMenu ).on('click', function(ev)
			{
				$items_with_subs.removeClass('hover');
			});
		}
		
		$items_with_subs.each(function(i, el)
		{
			var $li = jQuery(el),
				$a = $li.children('a'),
				$sub = $li.children('ul'),
				is_root_element = $li.parent().is('.navbar-nav');
			
			$li.addClass('has-sub');
			
			// Mobile Only
			$a.on('click', function(ev)
			{
				if(isxs())
				{
					ev.preventDefault();
				
					// Automatically will toggle other menu items in mobile view
					if(true)
					{
						sidebar_menu_close_items_siblings($li);
					}
					
					if($li.hasClass('expanded') || $li.hasClass('opened'))
						sidebar_menu_item_collapse($li, $sub);
					else
						sidebar_menu_item_expand($li, $sub);
				}
			});
			
			// Click To Expand
			if(click_to_expand)
			{
				$a.on('click', function(ev)
				{
					ev.preventDefault();
					
					if(isxs())
						return;
					
					// For parents only
					if(is_root_element)
					{
						$items_with_subs.filter(function(i, el){ return jQuery(el).parent().is('.navbar-nav'); }).not($li).removeClass('hover');
						$li.toggleClass('hover');
					}
					// Sub menus
					else
					{
						var sub_height;
						
						// To Expand
						if($li.hasClass('expanded') == false)
						{
							$li.addClass('expanded');
							$sub.addClass('is-visible');
							
							sub_height = $sub.outerHeight();
							
							$sub.height(0);
							
							TweenLite.to($sub, .15, {css: {height: sub_height}, ease: Sine.easeInOut, onComplete: function(){ $sub.attr('style', ''); }});
							
							// Hide Existing in the list
							$li.siblings().find('> ul.is-visible').not($sub).each(function(i, el)
							{
								var $el = jQuery(el);
								
								sub_height = $el.outerHeight();
								
								$el.removeClass('is-visible').height(sub_height);
								$el.parent().removeClass('expanded');
								
								TweenLite.to($el, .15, {css: {height: 0}, onComplete: function(){ $el.attr('style', ''); }});
							});
						}
						// To Collapse
						else
						{
							sub_height = $sub.outerHeight();
							
							$li.removeClass('expanded');
							$sub.removeClass('is-visible').height(sub_height);
							TweenLite.to($sub, .15, {css: {height: 0}, onComplete: function(){ $sub.attr('style', ''); }});
						}
					}
				});
			}
			// Hover To Expand
			else
			{	
				$li.hoverIntent({
					over: function()
					{
						if(isxs())
							return;
							
						if(is_root_element)
						{
							$li.addClass('hover');
						}
						else
						{
							$sub.addClass('is-visible');
							sub_height = $sub.outerHeight();
							
							$sub.height(0);
							
							TweenLite.to($sub, .25, {css: {height: sub_height}, ease: Sine.easeInOut, onComplete: function(){ $sub.attr('style', ''); }});
						}
					},
					out: function()
					{
						if(isxs())
							return;
							
						if(is_root_element)
						{
							$li.removeClass('hover');
						}
						else
						{
							sub_height = $sub.outerHeight();
							
							$li.removeClass('expanded');
							$sub.removeClass('is-visible').height(sub_height);
							TweenLite.to($sub, .25, {css: {height: 0}, onComplete: function(){ $sub.attr('style', ''); }});
						}
					},
					timeout: 200,
					interval: is_root_element ? 10 : 100
				});
			}
		});
	}
}


function stickFooterToBottom()
{
	public_vars.$mainFooter.add( public_vars.$mainContent ).add( public_vars.$sidebarMenu ).attr('style', '');
	
	if(isxs())
		return false;
		
	if(public_vars.$mainFooter.hasClass('sticky'))
	{
		var win_height				 = jQuery(window).height(),
			footer_height			= public_vars.$mainFooter.outerHeight(true),
			main_content_height	  = public_vars.$mainFooter.position().top + footer_height,
			main_content_height_only = main_content_height - footer_height,
			extra_height			 = public_vars.$horizontalNavbar.outerHeight();
		
		
		if(win_height > main_content_height - parseInt(public_vars.$mainFooter.css('marginTop'), 10))
		{
			public_vars.$mainFooter.css({
				marginTop: win_height - main_content_height - extra_height
			});
		}
	}
}


// Perfect scroll bar functions by Arlind Nushi
function ps_update(destroy_init)
{
	if(isxs())
		return;
		
	if(jQuery.isFunction(jQuery.fn.perfectScrollbar))
	{
		if(public_vars.$sidebarMenu.hasClass('collapsed'))
		{
			return;
		}
		
		public_vars.$sidebarMenu.find('.sidebar-menu-inner').perfectScrollbar('update');
		
		if(destroy_init)
		{
			ps_destroy();
			ps_init();
		}
	}
}


function ps_init()
{
	if(isxs())
		return;
		
	if(jQuery.isFunction(jQuery.fn.perfectScrollbar))
	{
		if(public_vars.$sidebarMenu.hasClass('collapsed') || ! public_vars.$sidebarMenu.hasClass('fixed'))
		{
			return;
		}
		
		public_vars.$sidebarMenu.find('.sidebar-menu-inner').perfectScrollbar({
			wheelSpeed: 2,
			wheelPropagation: public_vars.wheelPropagation
		});
	}
}

function ps_destroy()
{
	if(jQuery.isFunction(jQuery.fn.perfectScrollbar))
	{
		public_vars.$sidebarMenu.find('.sidebar-menu-inner').perfectScrollbar('destroy');
	}
}



// Radio and Check box replacement by Arlind Nushi
function cbr_replace()
{
	var $inputs = jQuery('input[type="checkbox"].cbr, input[type="radio"].cbr').filter(':not(.cbr-done)'),
		$wrapper = '<div class="cbr-replaced"><div class="cbr-input"></div><div class="cbr-state"><span></span></div></div>';
	
	$inputs.each(function(i, el)
	{
		var $el = jQuery(el),
			is_radio = $el.is(':radio'),
			is_checkbox = $el.is(':checkbox'),
			is_disabled = $el.is(':disabled'),
			styles = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'purple', 'blue', 'red', 'gray', 'pink', 'yellow', 'orange', 'turquoise'];
		
		if( ! is_radio && ! is_checkbox)
			return;
		
		$el.after( $wrapper );
		$el.addClass('cbr-done');
		
		var $wrp = $el.next();
		$wrp.find('.cbr-input').append( $el );
		
		if(is_radio)
			$wrp.addClass('cbr-radio');
		
		if(is_disabled)
			$wrp.addClass('cbr-disabled');
		
		if($el.is(':checked'))
		{
			$wrp.addClass('cbr-checked');
		}
		
		
		// Style apply
		jQuery.each(styles, function(key, val)
		{
			var cbr_class = 'cbr-' + val;
			
			if( $el.hasClass(cbr_class))
			{
				$wrp.addClass(cbr_class);
				$el.removeClass(cbr_class);
			}
		});
		
		
		// Events
		$wrp.on('click', function(ev)
		{
			if(is_radio && $el.prop('checked') || $wrp.parent().is('label'))
				return;
			
			if(jQuery(ev.target).is($el) == false)
			{
				$el.prop('checked', ! $el.is(':checked'));
				$el.trigger('change');
			}
		});
		
		$el.on('change', function(ev)
		{	
			$wrp.removeClass('cbr-checked');
			
			if($el.is(':checked'))
				$wrp.addClass('cbr-checked');
				
			cbr_recheck();
		});
	});
}


function cbr_recheck()
{
	var $inputs = jQuery("input.cbr-done");
	
	$inputs.each(function(i, el)
	{
		var $el = jQuery(el),
			is_radio = $el.is(':radio'),
			is_checkbox = $el.is(':checkbox'),
			is_disabled = $el.is(':disabled'),
			$wrp = $el.closest('.cbr-replaced');
		
		if(is_disabled)
			$wrp.addClass('cbr-disabled');
		
		if(is_radio && ! $el.prop('checked') && $wrp.hasClass('cbr-checked'))
		{
			$wrp.removeClass('cbr-checked');
		}
	});
}


// Element Attribute Helper
function attrDefault($el, data_var, default_val)
{
	if(typeof $el.data(data_var) != 'undefined')
	{
		return $el.data(data_var);
	}
	
	return default_val;
}


// Test function
function callback_test()
{
	alert("Callback function executed! No. of arguments: " + arguments.length + "\n\nSee console log for outputed of the arguments.");
	
	console.log(arguments);
}


// Date Formatter
function date(format, timestamp) {
	//	discuss at: http://phpjs.org/functions/date/
	// original by: Carlos R. L. Rodrigues (http://www.jsfromhell.com)
	// original by: gettimeofday
	//	parts by: Peter-Paul Koch (http://www.quirksmode.org/js/beat.html)
	// improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// improved by: MeEtc (http://yass.meetcweb.com)
	// improved by: Brad Touesnard
	// improved by: Tim Wiel
	// improved by: Bryan Elliott
	// improved by: David Randall
	// improved by: Theriault
	// improved by: Theriault
	// improved by: Brett Zamir (http://brett-zamir.me)
	// improved by: Theriault
	// improved by: Thomas Beaucourt (http://www.webapp.fr)
	// improved by: JT
	// improved by: Theriault
	// improved by: Rafał Kukawski (http://blog.kukawski.pl)
	// improved by: Theriault
	//	input by: Brett Zamir (http://brett-zamir.me)
	//	input by: majak
	//	input by: Alex
	//	input by: Martin
	//	input by: Alex Wilson
	//	input by: Haravikk
	// bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// bugfixed by: majak
	// bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// bugfixed by: Brett Zamir (http://brett-zamir.me)
	// bugfixed by: omid (http://phpjs.org/functions/380:380#comment_137122)
	// bugfixed by: Chris (http://www.devotis.nl/)
	//		note: Uses global: php_js to store the default timezone
	//		note: Although the function potentially allows timezone info (see notes), it currently does not set
	//		note: per a timezone specified by date_default_timezone_set(). Implementers might use
	//		note: this.php_js.currentTimezoneOffset and this.php_js.currentTimezoneDST set by that function
	//		note: in order to adjust the dates in this function (or our other date functions!) accordingly
	//	 example 1: date('H:m:s \\m \\i\\s \\m\\o\\n\\t\\h', 1062402400);
	//	 returns 1: '09:09:40 m is month'
	//	 example 2: date('F j, Y, g:i a', 1062462400);
	//	 returns 2: 'September 2, 2003, 2:26 am'
	//	 example 3: date('Y W o', 1062462400);
	//	 returns 3: '2003 36 2003'
	//	 example 4: x = date('Y m d', (new Date()).getTime()/1000);
	//	 example 4: (x+'').length == 10 // 2009 01 09
	//	 returns 4: true
	//	 example 5: date('W', 1104534000);
	//	 returns 5: '53'
	//	 example 6: date('B t', 1104534000);
	//	 returns 6: '999 31'
	//	 example 7: date('W U', 1293750000.82); // 2010-12-31
	//	 returns 7: '52 1293750000'
	//	 example 8: date('W', 1293836400); // 2011-01-01
	//	 returns 8: '52'
	//	 example 9: date('W Y-m-d', 1293974054); // 2011-01-02
	//	 returns 9: '52 2011-01-02'

	var that = this;
	var jsdate, f;
	// Keep this here (works, but for code commented-out below for file size reasons)
	// var tal= [];
	var txt_words = [
	'Sun', 'Mon', 'Tues', 'Wednes', 'Thurs', 'Fri', 'Satur',
	'January', 'February', 'March', 'April', 'May', 'June',
	'July', 'August', 'September', 'October', 'November', 'December'
	];
	// trailing backslash -> (dropped)
	// a backslash followed by any character (including backslash) -> the character
	// empty string -> empty string
	var formatChr = /\\?(.?)/gi;
	var formatChrCb = function (t, s) {
	return f[t] ? f[t]() : s;
	};
	var _pad = function (n, c) {
	n = String(n);
	while (n.length < c) {
		n = '0' + n;
	}
	return n;
	};
	f = {
	// Day
	d: function () {
		// Day of month w/leading 0; 01..31
		return _pad(f.j(), 2);
	},
	D: function () {
		// Shorthand day name; Mon...Sun
		return f.l()
		.slice(0, 3);
	},
	j: function () {
		// Day of month; 1..31
		return jsdate.getDate();
	},
	l: function () {
		// Full day name; Monday...Sunday
		return txt_words[f.w()] + 'day';
	},
	N: function () {
		// ISO-8601 day of week; 1[Mon]..7[Sun]
		return f.w() || 7;
	},
	S: function () {
		// Ordinal suffix for day of month; st, nd, rd, th
		var j = f.j();
		var i = j % 10;
		if (i <= 3 && parseInt((j % 100) / 10, 10) == 1) {
		i = 0;
		}
		return ['st', 'nd', 'rd'][i - 1] || 'th';
	},
	w: function () {
		// Day of week; 0[Sun]..6[Sat]
		return jsdate.getDay();
	},
	z: function () {
		// Day of year; 0..365
		var a = new Date(f.Y(), f.n() - 1, f.j());
		var b = new Date(f.Y(), 0, 1);
		return Math.round((a - b) / 864e5);
	},

	// Week
	W: function () {
		// ISO-8601 week number
		var a = new Date(f.Y(), f.n() - 1, f.j() - f.N() + 3);
		var b = new Date(a.getFullYear(), 0, 4);
		return _pad(1 + Math.round((a - b) / 864e5 / 7), 2);
	},

	// Month
	F: function () {
		// Full month name; January...December
		return txt_words[6 + f.n()];
	},
	m: function () {
		// Month w/leading 0; 01...12
		return _pad(f.n(), 2);
	},
	M: function () {
		// Shorthand month name; Jan...Dec
		return f.F()
		.slice(0, 3);
	},
	n: function () {
		// Month; 1...12
		return jsdate.getMonth() + 1;
	},
	t: function () {
		// Days in month; 28...31
		return (new Date(f.Y(), f.n(), 0))
		.getDate();
	},

	// Year
	L: function () {
		// Is leap year?; 0 or 1
		var j = f.Y();
		return j % 4 === 0 & j % 100 !== 0 | j % 400 === 0;
	},
	o: function () {
		// ISO-8601 year
		var n = f.n();
		var W = f.W();
		var Y = f.Y();
		return Y + (n === 12 && W < 9 ? 1 : n === 1 && W > 9 ? -1 : 0);
	},
	Y: function () {
		// Full year; e.g. 1980...2010
		return jsdate.getFullYear();
	},
	y: function () {
		// Last two digits of year; 00...99
		return f.Y()
		.toString()
		.slice(-2);
	},

	// Time
	a: function () {
		// am or pm
		return jsdate.getHours() > 11 ? 'pm' : 'am';
	},
	A: function () {
		// AM or PM
		return f.a()
		.toUpperCase();
	},
	B: function () {
		// Swatch Internet time; 000..999
		var H = jsdate.getUTCHours() * 36e2;
		// Hours
		var i = jsdate.getUTCMinutes() * 60;
		// Minutes
		// Seconds
		var s = jsdate.getUTCSeconds();
		return _pad(Math.floor((H + i + s + 36e2) / 86.4) % 1e3, 3);
	},
	g: function () {
		// 12-Hours; 1..12
		return f.G() % 12 || 12;
	},
	G: function () {
		// 24-Hours; 0..23
		return jsdate.getHours();
	},
	h: function () {
		// 12-Hours w/leading 0; 01..12
		return _pad(f.g(), 2);
	},
	H: function () {
		// 24-Hours w/leading 0; 00..23
		return _pad(f.G(), 2);
	},
	i: function () {
		// Minutes w/leading 0; 00..59
		return _pad(jsdate.getMinutes(), 2);
	},
	s: function () {
		// Seconds w/leading 0; 00..59
		return _pad(jsdate.getSeconds(), 2);
	},
	u: function () {
		// Microseconds; 000000-999000
		return _pad(jsdate.getMilliseconds() * 1000, 6);
	},

	// Timezone
	e: function () {
		// Timezone identifier; e.g. Atlantic/Azores, ...
		// The following works, but requires inclusion of the very large
		// timezone_abbreviations_list() function.
		/*				return that.date_default_timezone_get();
		 */
		throw 'Not supported (see source code of date() for timezone on how to add support)';
	},
	I: function () {
		// DST observed?; 0 or 1
		// Compares Jan 1 minus Jan 1 UTC to Jul 1 minus Jul 1 UTC.
		// If they are not equal, then DST is observed.
		var a = new Date(f.Y(), 0);
		// Jan 1
		var c = Date.UTC(f.Y(), 0);
		// Jan 1 UTC
		var b = new Date(f.Y(), 6);
		// Jul 1
		// Jul 1 UTC
		var d = Date.UTC(f.Y(), 6);
		return ((a - c) !== (b - d)) ? 1 : 0;
	},
	O: function () {
		// Difference to GMT in hour format; e.g. +0200
		var tzo = jsdate.getTimezoneOffset();
		var a = Math.abs(tzo);
		return (tzo > 0 ? '-' : '+') + _pad(Math.floor(a / 60) * 100 + a % 60, 4);
	},
	P: function () {
		// Difference to GMT w/colon; e.g. +02:00
		var O = f.O();
		return (O.substr(0, 3) + ':' + O.substr(3, 2));
	},
	T: function () {
		// Timezone abbreviation; e.g. EST, MDT, ...
		// The following works, but requires inclusion of the very
		// large timezone_abbreviations_list() function.
		/*				var abbr, i, os, _default;
		if (!tal.length) {
		tal = that.timezone_abbreviations_list();
		}
		if (that.php_js && that.php_js.default_timezone) {
		_default = that.php_js.default_timezone;
		for (abbr in tal) {
			for (i = 0; i < tal[abbr].length; i++) {
			if (tal[abbr][i].timezone_id === _default) {
				return abbr.toUpperCase();
			}
			}
		}
		}
		for (abbr in tal) {
		for (i = 0; i < tal[abbr].length; i++) {
			os = -jsdate.getTimezoneOffset() * 60;
			if (tal[abbr][i].offset === os) {
			return abbr.toUpperCase();
			}
		}
		}
		*/
		return 'UTC';
	},
	Z: function () {
		// Timezone offset in seconds (-43200...50400)
		return -jsdate.getTimezoneOffset() * 60;
	},

	// Full Date/Time
	c: function () {
		// ISO-8601 date.
		return 'Y-m-d\\TH:i:sP'.replace(formatChr, formatChrCb);
	},
	r: function () {
		// RFC 2822
		return 'D, d M Y H:i:s O'.replace(formatChr, formatChrCb);
	},
	U: function () {
		// Seconds since UNIX epoch
		return jsdate / 1000 | 0;
	}
	};
	
	this.date = function (format, timestamp) {
		that = this;
		jsdate = (timestamp === undefined ? new Date() : // Not provided
			(timestamp instanceof Date) ? new Date(timestamp) : // JS Date()
			new Date(timestamp * 1000) // UNIX timestamp (auto-convert to int)
		);
		return format.replace(formatChr, formatChrCb);
	};
	return this.date(format, timestamp);
}





/**
 *	Toggles
 *
 *	Non-animation
 */


;(function($, window, undefined)
{
    "use strict";

    $(document).ready(function()
    {

        // Chat Toggler
        $('a[data-toggle="chat"]').each(function(i, el)
        {
            $(el).on('click', function(ev)
            {
                ev.preventDefault();

                public_vars.$body.toggleClass('chat-open');

                if($.isFunction($.fn.perfectScrollbar))
                {
                    setTimeout(function()
                    {
                        public_vars.$chat.find('.chat_inner').perfectScrollbar('update');
                        $(window).trigger('xenon.resize');
                    }, 1);
                }
            });
        });


        // Settings Pane Toggler
        $('a[data-toggle="settings-pane"]').each(function(i, el)
        {
            $(el).on('click', function(ev)
            {
                ev.preventDefault();

                var use_animation = attrDefault($(el), 'animate', false) && ! isxs();

                var scroll = {
                    top: $(document).scrollTop(),
                    toTop: 0
                };

                if(public_vars.$body.hasClass('settings-pane-open'))
                {
                    scroll.toTop = scroll.top;
                }

                TweenMax.to(scroll, (use_animation ? .1 : 0), {top: scroll.toTop, roundProps: ['top'], ease: scroll.toTop < 10 ? null : Sine.easeOut, onUpdate: function()
                    {
                        $(window).scrollTop( scroll.top );
                    },
                    onComplete: function()
                    {
                        if(use_animation)
                        {
                            // With Animation
                            public_vars.$settingsPaneIn.addClass('with-animation');

                            // Opening
                            if( ! public_vars.$settingsPane.is(':visible'))
                            {
                                public_vars.$body.addClass('settings-pane-open');

                                var height = public_vars.$settingsPane.outerHeight(true);

                                public_vars.$settingsPane.css({
                                    height: 0
                                });

                                TweenMax.to(public_vars.$settingsPane, .25, {css: {height: height}, ease: Circ.easeInOut, onComplete: function()
                                    {
                                        public_vars.$settingsPane.css({height: ''});
                                    }});

                                public_vars.$settingsPaneIn.addClass('visible');
                            }
                            // Closing
                            else
                            {
                                public_vars.$settingsPaneIn.addClass('closing');

                                TweenMax.to(public_vars.$settingsPane, .25, {css: {height: 0}, delay: .15, ease: Power1.easeInOut, onComplete: function()
                                    {
                                        public_vars.$body.removeClass('settings-pane-open');
                                        public_vars.$settingsPane.css({height: ''});
                                        public_vars.$settingsPaneIn.removeClass('closing visible');
                                    }});
                            }
                        }
                        else
                        {
                            // Without Animation
                            public_vars.$body.toggleClass('settings-pane-open');
                            public_vars.$settingsPaneIn.removeClass('visible');
                            public_vars.$settingsPaneIn.removeClass('with-animation');
                        }
                    }
                });
            });
        });



        // Sidebar Toggle
        $('a[data-toggle="sidebar"]').each(function(i, el)
        {
            $(el).on('click', function(ev)
            {
                ev.preventDefault();

                if(public_vars.$sidebarMenu.hasClass('collapsed'))
                {
                    public_vars.$sidebarMenu.removeClass('collapsed');
                    ps_init();
                }
                else
                {
                    public_vars.$sidebarMenu.addClass('collapsed');
                    ps_destroy();
                }

                $(window).trigger('xenon.resize');
            });
        });



        // Mobile Menu Trigger
        $('a[data-toggle="mobile-menu"]').on('click', function(ev)
        {
            ev.preventDefault();

            public_vars.$mainMenu.toggleClass('mobile-is-visible');
            ps_destroy();
        });



        // Mobile Menu Trigger for Horizontal Menu
        $('a[data-toggle="mobile-menu-horizontal"]').on('click', function(ev)
        {
            ev.preventDefault();

            public_vars.$horizontalMenu.toggleClass('mobile-is-visible');

        });



        // Mobile Menu Trigger for Sidebar & Horizontal Menu
        $('a[data-toggle="mobile-menu-both"]').on('click', function(ev)
        {
            ev.preventDefault();

            public_vars.$mainMenu.toggleClass('mobile-is-visible both-menus-visible');
            public_vars.$horizontalMenu.toggleClass('mobile-is-visible both-menus-visible');

        });



        // Mobile User Info Menu Trigger
        $('a[data-toggle="user-info-menu"]').on('click', function(ev)
        {
            ev.preventDefault();

            public_vars.$userInfoMenu.toggleClass('mobile-is-visible');

        });



        // Mobile User Info Menu Trigger for Horizontal Menu
        $('a[data-toggle="user-info-menu-horizontal"]').on('click', function(ev)
        {
            ev.preventDefault();

            public_vars.$userInfoMenuHor.find('.nav.nav-userinfo').toggleClass('mobile-is-visible');

        });



        // Panel Close
        $('body').on('click', '.panel a[data-toggle="remove"]', function(ev)
        {
            ev.preventDefault();

            var $panel = $(this).closest('.panel'),
                $panel_parent = $panel.parent();

            $panel.remove();

            if($panel_parent.children().length == 0)
            {
                $panel_parent.remove();
            }
        });



        // Panel Reload
        $('body').on('click', '.panel a[data-toggle="reload"]', function(ev)
        {
            ev.preventDefault();

            var $panel = $(this).closest('.panel');

            // This is just a simulation, nothing is going to be reloaded
            $panel.append('<div class="panel-disabled"><div class="loader-1"></div></div>');

            var $pd = $panel.find('.panel-disabled');

            setTimeout(function()
            {
                $pd.fadeOut('fast', function()
                {
                    $pd.remove();
                });

            }, 500 + 300 * (Math.random() * 5));
        });



        // Panel Expand/Collapse Toggle
        $('body').on('click', '.panel a[data-toggle="panel"]', function(ev)
        {
            ev.preventDefault();

            var $panel = $(this).closest('.panel');

            $panel.toggleClass('collapsed');
        });



        // Loading Text toggle
        $('[data-loading-text]').each(function(i, el) // Temporary for demo purpose only
        {
            var $this = $(el);

            $this.on('click', function(ev)
            {
                $this.button('loading');

                setTimeout(function(){ $this.button('reset'); }, 1800);
            });
        });




        // Popovers and tooltips
        $('[data-toggle="popover"]').each(function(i, el)
        {
            var $this = $(el),
                placement = attrDefault($this, 'placement', 'right'),
                trigger = attrDefault($this, 'trigger', 'click'),
                popover_class = $this.get(0).className.match(/(popover-[a-z0-9]+)/i);

            $this.popover({
                placement: placement,
                trigger: trigger
            });

            if(popover_class)
            {
                $this.removeClass(popover_class[1]);

                $this.on('show.bs.popover', function(ev)
                {
                    setTimeout(function()
                    {
                        var $popover = $this.next();
                        $popover.addClass(popover_class[1]);

                    }, 0);
                });
            }
        });

        $('[data-toggle="tooltip"]').each(function(i, el)
        {
            var $this = $(el),
                placement = attrDefault($this, 'placement', 'top'),
                trigger = attrDefault($this, 'trigger', 'hover'),
                tooltip_class = $this.get(0).className.match(/(tooltip-[a-z0-9]+)/i);

            $this.tooltip({
                placement: placement,
                trigger: trigger
            });

            if(tooltip_class)
            {
                $this.removeClass(tooltip_class[1]);

                $this.on('show.bs.tooltip', function(ev)
                {
                    setTimeout(function()
                    {
                        var $tooltip = $this.next();
                        $tooltip.addClass(tooltip_class[1]);

                    }, 0);
                });
            }
        });

    });

})(jQuery, window);







/**
 *	Xenon API Functions
 *
 *	Theme by: www.laborator.co
 **/


function rtl() // checks whether the content is in RTL mode
{
    if(typeof window.isRTL == 'boolean')
        return window.isRTL;

    window.isRTL = jQuery("html").get(0).dir == 'rtl' ? true : false;

    return window.isRTL;
}



// Page Loader
function show_loading_bar(options)
{
    var defaults = {
        pct: 0,
        delay: 1.3,
        wait: 0,
        before: function(){},
        finish: function(){},
        resetOnEnd: true
    };

    if(typeof options == 'object')
        defaults = jQuery.extend(defaults, options);
    else
    if(typeof options == 'number')
        defaults.pct = options;


    if(defaults.pct > 100)
        defaults.pct = 100;
    else
    if(defaults.pct < 0)
        defaults.pct = 0;

    var $ = jQuery,
        $loading_bar = $(".xenon-loading-bar");

    if($loading_bar.length == 0)
    {
        $loading_bar = $('<div class="xenon-loading-bar progress-is-hidden"><span data-pct="0"></span></div>');
        public_vars.$body.append( $loading_bar );
    }

    var $pct = $loading_bar.find('span'),
        current_pct = $pct.data('pct'),
        is_regress = current_pct > defaults.pct;


    defaults.before(current_pct);

    TweenMax.to($pct, defaults.delay, {css: {width: defaults.pct + '%'}, delay: defaults.wait, ease: is_regress ? Expo.easeOut : Expo.easeIn,
        onStart: function()
        {
            $loading_bar.removeClass('progress-is-hidden');
        },
        onComplete: function()
        {
            var pct = $pct.data('pct');

            if(pct == 100 && defaults.resetOnEnd)
            {
                hide_loading_bar();
            }

            defaults.finish(pct);
        },
        onUpdate: function()
        {
            $pct.data('pct', parseInt($pct.get(0).style.width, 10));
        }});
}

function hide_loading_bar()
{
    var $ = jQuery,
        $loading_bar = $(".xenon-loading-bar"),
        $pct = $loading_bar.find('span');

    $loading_bar.addClass('progress-is-hidden');
    $pct.width(0).data('pct', 0);
}






/**
 *
 *	Bunch of scripts included in one file to reduce number HTTP requests
 *
 */



/*!
	Autosize v1.18.9 - 2014-05-27
	Automatically adjust textarea height based on user input.
	(c) 2014 Jack Moore - http://www.jacklmoore.com/autosize
	license: http://www.opensource.org/licenses/mit-license.php
*/
(function(e){var t,o={className:"autosizejs",id:"autosizejs",append:"\n",callback:!1,resizeDelay:10,placeholder:!0},i='<textarea tabindex="-1" style="position:absolute; top:-999px; left:0; right:auto; bottom:auto; border:0; padding: 0; -moz-box-sizing:content-box; -webkit-box-sizing:content-box; box-sizing:content-box; word-wrap:break-word; height:0 !important; min-height:0 !important; overflow:hidden; transition:none; -webkit-transition:none; -moz-transition:none;"/>',n=["fontFamily","fontSize","fontWeight","fontStyle","letterSpacing","textTransform","wordSpacing","textIndent"],s=e(i).data("autosize",!0)[0];s.style.lineHeight="99px","99px"===e(s).css("lineHeight")&&n.push("lineHeight"),s.style.lineHeight="",e.fn.autosize=function(i){return this.length?(i=e.extend({},o,i||{}),s.parentNode!==document.body&&e(document.body).append(s),this.each(function(){function o(){var t,o=window.getComputedStyle?window.getComputedStyle(u,null):!1;o?(t=u.getBoundingClientRect().width,(0===t||"number"!=typeof t)&&(t=parseInt(o.width,10)),e.each(["paddingLeft","paddingRight","borderLeftWidth","borderRightWidth"],function(e,i){t-=parseInt(o[i],10)})):t=p.width(),s.style.width=Math.max(t,0)+"px"}function a(){var a={};if(t=u,s.className=i.className,s.id=i.id,d=parseInt(p.css("maxHeight"),10),e.each(n,function(e,t){a[t]=p.css(t)}),e(s).css(a).attr("wrap",p.attr("wrap")),o(),window.chrome){var r=u.style.width;u.style.width="0px",u.offsetWidth,u.style.width=r}}function r(){var e,n;t!==u?a():o(),s.value=!u.value&&i.placeholder?(p.attr("placeholder")||"")+i.append:u.value+i.append,s.style.overflowY=u.style.overflowY,n=parseInt(u.style.height,10),s.scrollTop=0,s.scrollTop=9e4,e=s.scrollTop,d&&e>d?(u.style.overflowY="scroll",e=d):(u.style.overflowY="hidden",c>e&&(e=c)),e+=w,n!==e&&(u.style.height=e+"px",f&&i.callback.call(u,u))}function l(){clearTimeout(h),h=setTimeout(function(){var e=p.width();e!==g&&(g=e,r())},parseInt(i.resizeDelay,10))}var d,c,h,u=this,p=e(u),w=0,f=e.isFunction(i.callback),z={height:u.style.height,overflow:u.style.overflow,overflowY:u.style.overflowY,wordWrap:u.style.wordWrap,resize:u.style.resize},g=p.width(),y=p.css("resize");p.data("autosize")||(p.data("autosize",!0),("border-box"===p.css("box-sizing")||"border-box"===p.css("-moz-box-sizing")||"border-box"===p.css("-webkit-box-sizing"))&&(w=p.outerHeight()-p.height()),c=Math.max(parseInt(p.css("minHeight"),10)-w||0,p.height()),p.css({overflow:"hidden",overflowY:"hidden",wordWrap:"break-word"}),"vertical"===y?p.css("resize","none"):"both"===y&&p.css("resize","horizontal"),"onpropertychange"in u?"oninput"in u?p.on("input.autosize keyup.autosize",r):p.on("propertychange.autosize",function(){"value"===event.propertyName&&r()}):p.on("input.autosize",r),i.resizeDelay!==!1&&e(window).on("resize.autosize",l),p.on("autosize.resize",r),p.on("autosize.resizeIncludeStyle",function(){t=null,r()}),p.on("autosize.destroy",function(){t=null,clearTimeout(h),e(window).off("resize",l),p.off("autosize").off(".autosize").css(z).removeData("autosize")}),r())})):this}})(window.jQuery||window.$);


/* Scroll Monitor */
(function(e){if(typeof define!=="undefined"&&define.amd){define(["jquery"],e)}else if(typeof module!=="undefined"&&module.exports){var t=require("jquery");module.exports=e(t)}else{window.scrollMonitor=e(jQuery)}})(function(e){function m(){return window.innerHeight||document.documentElement.clientHeight}function y(){t.viewportTop=n.scrollTop();t.viewportBottom=t.viewportTop+t.viewportHeight;t.documentHeight=r.height();if(t.documentHeight!==d){g=i.length;while(g--){i[g].recalculateLocation()}d=t.documentHeight}}function b(){t.viewportHeight=m();y();x()}function E(){clearTimeout(w);w=setTimeout(b,100)}function x(){S=i.length;while(S--){i[S].update()}S=i.length;while(S--){i[S].triggerCallbacks()}}function T(n,r){function x(e){if(e.length===0){return}E=e.length;while(E--){S=e[E];S.callback.call(i,v);if(S.isOne){e.splice(E,1)}}}var i=this;this.watchItem=n;if(!r){this.offsets=p}else if(r===+r){this.offsets={top:r,bottom:r}}else{this.offsets=e.extend({},p,r)}this.callbacks={};for(var d=0,m=h.length;d<m;d++){i.callbacks[h[d]]=[]}this.locked=false;var g;var y;var b;var w;var E;var S;this.triggerCallbacks=function(){if(this.isInViewport&&!g){x(this.callbacks[o])}if(this.isFullyInViewport&&!y){x(this.callbacks[u])}if(this.isAboveViewport!==b&&this.isBelowViewport!==w){x(this.callbacks[s]);if(!y&&!this.isFullyInViewport){x(this.callbacks[u]);x(this.callbacks[f])}if(!g&&!this.isInViewport){x(this.callbacks[o]);x(this.callbacks[a])}}if(!this.isFullyInViewport&&y){x(this.callbacks[f])}if(!this.isInViewport&&g){x(this.callbacks[a])}if(this.isInViewport!==g){x(this.callbacks[s])}switch(true){case g!==this.isInViewport:case y!==this.isFullyInViewport:case b!==this.isAboveViewport:case w!==this.isBelowViewport:x(this.callbacks[c])}g=this.isInViewport;y=this.isFullyInViewport;b=this.isAboveViewport;w=this.isBelowViewport};this.recalculateLocation=function(){if(this.locked){return}var n=this.top;var r=this.bottom;if(this.watchItem.nodeName){var i=this.watchItem.style.display;if(i==="none"){this.watchItem.style.display=""}var s=e(this.watchItem).offset();this.top=s.top;this.bottom=s.top+this.watchItem.offsetHeight;if(i==="none"){this.watchItem.style.display=i}}else if(this.watchItem===+this.watchItem){if(this.watchItem>0){this.top=this.bottom=this.watchItem}else{this.top=this.bottom=t.documentHeight-this.watchItem}}else{this.top=this.watchItem.top;this.bottom=this.watchItem.bottom}this.top-=this.offsets.top;this.bottom+=this.offsets.bottom;this.height=this.bottom-this.top;if((n!==undefined||r!==undefined)&&(this.top!==n||this.bottom!==r)){x(this.callbacks[l])}};this.recalculateLocation();this.update();g=this.isInViewport;y=this.isFullyInViewport;b=this.isAboveViewport;w=this.isBelowViewport}function O(e){v=e;y();x()}var t={};var n=e(window);var r=e(document);var i=[];var s="visibilityChange";var o="enterViewport";var u="fullyEnterViewport";var a="exitViewport";var f="partiallyExitViewport";var l="locationChange";var c="stateChange";var h=[s,o,u,a,f,l,c];var p={top:0,bottom:0};t.viewportTop;t.viewportBottom;t.documentHeight;t.viewportHeight=m();var d;var v;var g;var w;var S;T.prototype={on:function(e,t,n){switch(true){case e===s&&!this.isInViewport&&this.isAboveViewport:case e===o&&this.isInViewport:case e===u&&this.isFullyInViewport:case e===a&&this.isAboveViewport&&!this.isInViewport:case e===f&&this.isAboveViewport:t();if(n){return}}if(this.callbacks[e]){this.callbacks[e].push({callback:t,isOne:n})}else{throw new Error("Tried to add a scroll monitor listener of type "+e+". Your options are: "+h.join(", "))}},off:function(e,t){if(this.callbacks[e]){for(var n=0,r;r=this.callbacks[e][n];n++){if(r.callback===t){this.callbacks[e].splice(n,1);break}}}else{throw new Error("Tried to remove a scroll monitor listener of type "+e+". Your options are: "+h.join(", "))}},one:function(e,t){this.on(e,t,true)},recalculateSize:function(){this.height=this.watchItem.offsetHeight+this.offsets.top+this.offsets.bottom;this.bottom=this.top+this.height},update:function(){this.isAboveViewport=this.top<t.viewportTop;this.isBelowViewport=this.bottom>t.viewportBottom;this.isInViewport=this.top<=t.viewportBottom&&this.bottom>=t.viewportTop;this.isFullyInViewport=this.top>=t.viewportTop&&this.bottom<=t.viewportBottom||this.isAboveViewport&&this.isBelowViewport},destroy:function(){var e=i.indexOf(this),t=this;i.splice(e,1);for(var n=0,r=h.length;n<r;n++){t.callbacks[h[n]].length=0}},lock:function(){this.locked=true},unlock:function(){this.locked=false}};var N=function(e){return function(t,n){this.on.call(this,e,t,n)}};for(var C=0,k=h.length;C<k;C++){var L=h[C];T.prototype[L]=N(L)}try{y()}catch(A){e(y)}n.on("scroll",O);n.on("resize",E);t.beget=t.create=function(t,n){if(typeof t==="string"){t=e(t)[0]}if(t instanceof e){t=t[0]}var r=new T(t,n);i.push(r);r.update();return r};t.update=function(){v=null;y();x()};t.recalculateLocations=function(){t.documentHeight=0;t.update()};return t})



/* Count It Up */
function countUp(a,b,c,d,e,f){for(var g=0,h=["webkit","moz","ms","o"],i=0;i<h.length&&!window.requestAnimationFrame;++i)window.requestAnimationFrame=window[h[i]+"RequestAnimationFrame"],window.cancelAnimationFrame=window[h[i]+"CancelAnimationFrame"]||window[h[i]+"CancelRequestAnimationFrame"];window.requestAnimationFrame||(window.requestAnimationFrame=function(a){var c=(new Date).getTime(),d=Math.max(0,16-(c-g)),e=window.setTimeout(function(){a(c+d)},d);return g=c+d,e}),window.cancelAnimationFrame||(window.cancelAnimationFrame=function(a){clearTimeout(a)}),this.options=f||{useEasing:!0,useGrouping:!0,separator:",",decimal:"."},""==this.options.separator&&(this.options.useGrouping=!1),null==this.options.prefix&&(this.options.prefix=""),null==this.options.suffix&&(this.options.suffix="");var j=this;this.d="string"==typeof a?document.getElementById(a):a,this.startVal=Number(b),this.endVal=Number(c),this.countDown=this.startVal>this.endVal?!0:!1,this.startTime=null,this.timestamp=null,this.remaining=null,this.frameVal=this.startVal,this.rAF=null,this.decimals=Math.max(0,d||0),this.dec=Math.pow(10,this.decimals),this.duration=1e3*e||2e3,this.version=function(){return"1.3.1"},this.printValue=function(a){var b=isNaN(a)?"--":j.formatNumber(a);"INPUT"==j.d.tagName?this.d.value=b:this.d.innerHTML=b},this.easeOutExpo=function(a,b,c,d){return 1024*c*(-Math.pow(2,-10*a/d)+1)/1023+b},this.count=function(a){null===j.startTime&&(j.startTime=a),j.timestamp=a;var b=a-j.startTime;if(j.remaining=j.duration-b,j.options.useEasing)if(j.countDown){var c=j.easeOutExpo(b,0,j.startVal-j.endVal,j.duration);j.frameVal=j.startVal-c}else j.frameVal=j.easeOutExpo(b,j.startVal,j.endVal-j.startVal,j.duration);else if(j.countDown){var c=(j.startVal-j.endVal)*(b/j.duration);j.frameVal=j.startVal-c}else j.frameVal=j.startVal+(j.endVal-j.startVal)*(b/j.duration);j.frameVal=j.countDown?j.frameVal<j.endVal?j.endVal:j.frameVal:j.frameVal>j.endVal?j.endVal:j.frameVal,j.frameVal=Math.round(j.frameVal*j.dec)/j.dec,j.printValue(j.frameVal),b<j.duration?j.rAF=requestAnimationFrame(j.count):null!=j.callback&&j.callback()},this.start=function(a){return j.callback=a,isNaN(j.endVal)||isNaN(j.startVal)?(console.log("countUp error: startVal or endVal is not a number"),j.printValue()):j.rAF=requestAnimationFrame(j.count),!1},this.stop=function(){cancelAnimationFrame(j.rAF)},this.reset=function(){j.startTime=null,j.startVal=b,cancelAnimationFrame(j.rAF),j.printValue(j.startVal)},this.resume=function(){j.stop(),j.startTime=null,j.duration=j.remaining,j.startVal=j.frameVal,requestAnimationFrame(j.count)},this.formatNumber=function(a){a=a.toFixed(j.decimals),a+="";var b,c,d,e;if(b=a.split("."),c=b[0],d=b.length>1?j.options.decimal+b[1]:"",e=/(\d+)(\d{3})/,j.options.useGrouping)for(;e.test(c);)c=c.replace(e,"$1"+j.options.separator+"$2");return j.options.prefix+c+d+j.options.suffix},j.printValue(j.startVal)}


/*! perfect-scrollbar - v0.5.2
* http://noraesae.github.com/perfect-scrollbar/
* Copyright (c) 2014 Hyunje Alex Jun; Licensed MIT */
(function(e){"use strict";"function"==typeof define&&define.amd?define(["jquery"],e):"object"==typeof exports?e(require("jquery")):e(jQuery)})(function(e){"use strict";var t={wheelSpeed:1,wheelPropagation:!1,minScrollbarLength:null,maxScrollbarLength:null,useBothWheelAxes:!1,useKeyboard:!0,suppressScrollX:!1,suppressScrollY:!1,scrollXMarginOffset:0,scrollYMarginOffset:0,includePadding:!1},o=function(){var e=0;return function(){var t=e;return e+=1,".perfect-scrollbar-"+t}}();e.fn.perfectScrollbar=function(n,r){return this.each(function(){var l=e.extend(!0,{},t),a=e(this);if("object"==typeof n?e.extend(!0,l,n):r=n,"update"===r)return a.data("perfect-scrollbar-update")&&a.data("perfect-scrollbar-update")(),a;if("destroy"===r)return a.data("perfect-scrollbar-destroy")&&a.data("perfect-scrollbar-destroy")(),a;if(a.data("perfect-scrollbar"))return a.data("perfect-scrollbar");a.addClass("ps-container");var s,i,c,d,u,p,f,v,h,b,g=e("<div class='ps-scrollbar-x-rail'></div>").appendTo(a),m=e("<div class='ps-scrollbar-y-rail'></div>").appendTo(a),w=e("<div class='ps-scrollbar-x'></div>").appendTo(g),T=e("<div class='ps-scrollbar-y'></div>").appendTo(m),L=parseInt(g.css("bottom"),10),y=L===L,I=y?null:parseInt(g.css("top"),10),S=parseInt(m.css("right"),10),C=S===S,x=C?null:parseInt(m.css("left"),10),D="rtl"===a.css("direction"),X=o(),Y=parseInt(g.css("borderLeftWidth"),10)+parseInt(g.css("borderRightWidth"),10),P=parseInt(g.css("borderTopWidth"),10)+parseInt(g.css("borderBottomWidth"),10),k=function(e,t){var o=e+t,n=d-h;b=0>o?0:o>n?n:o;var r=parseInt(b*(p-d)/(d-h),10);a.scrollTop(r)},E=function(e,t){var o=e+t,n=c-f;v=0>o?0:o>n?n:o;var r=parseInt(v*(u-c)/(c-f),10);a.scrollLeft(r)},M=function(e){return l.minScrollbarLength&&(e=Math.max(e,l.minScrollbarLength)),l.maxScrollbarLength&&(e=Math.min(e,l.maxScrollbarLength)),e},W=function(){var e={width:c,display:s?"inherit":"none"};e.left=D?a.scrollLeft()+c-u:a.scrollLeft(),y?e.bottom=L-a.scrollTop():e.top=I+a.scrollTop(),g.css(e);var t={top:a.scrollTop(),height:d,display:i?"inherit":"none"};C?t.right=D?u-a.scrollLeft()-S-T.outerWidth():S-a.scrollLeft():t.left=D?a.scrollLeft()+2*c-u-x-T.outerWidth():x+a.scrollLeft(),m.css(t),w.css({left:v,width:f-Y}),T.css({top:b,height:h-P}),s?a.addClass("ps-active-x"):a.removeClass("ps-active-x"),i?a.addClass("ps-active-y"):a.removeClass("ps-active-y")},j=function(){g.hide(),m.hide(),c=l.includePadding?a.innerWidth():a.width(),d=l.includePadding?a.innerHeight():a.height(),u=a.prop("scrollWidth"),p=a.prop("scrollHeight"),!l.suppressScrollX&&u>c+l.scrollXMarginOffset?(s=!0,f=M(parseInt(c*c/u,10)),v=parseInt(a.scrollLeft()*(c-f)/(u-c),10)):(s=!1,f=0,v=0,a.scrollLeft(0)),!l.suppressScrollY&&p>d+l.scrollYMarginOffset?(i=!0,h=M(parseInt(d*d/p,10)),b=parseInt(a.scrollTop()*(d-h)/(p-d),10)):(i=!1,h=0,b=0,a.scrollTop(0)),b>=d-h&&(b=d-h),v>=c-f&&(v=c-f),W(),l.suppressScrollX||g.show(),l.suppressScrollY||m.show()},O=function(){var t,o;w.bind("mousedown"+X,function(e){o=e.pageX,t=w.position().left,g.addClass("in-scrolling"),e.stopPropagation(),e.preventDefault()}),e(document).bind("mousemove"+X,function(e){g.hasClass("in-scrolling")&&(E(t,e.pageX-o),j(),e.stopPropagation(),e.preventDefault())}),e(document).bind("mouseup"+X,function(){g.hasClass("in-scrolling")&&g.removeClass("in-scrolling")}),t=o=null},q=function(){var t,o;T.bind("mousedown"+X,function(e){o=e.pageY,t=T.position().top,m.addClass("in-scrolling"),e.stopPropagation(),e.preventDefault()}),e(document).bind("mousemove"+X,function(e){m.hasClass("in-scrolling")&&(k(t,e.pageY-o),j(),e.stopPropagation(),e.preventDefault())}),e(document).bind("mouseup"+X,function(){m.hasClass("in-scrolling")&&m.removeClass("in-scrolling")}),t=o=null},A=function(e,t){var o=a.scrollTop();if(0===e){if(!i)return!1;if(0===o&&t>0||o>=p-d&&0>t)return!l.wheelPropagation}var n=a.scrollLeft();if(0===t){if(!s)return!1;if(0===n&&0>e||n>=u-c&&e>0)return!l.wheelPropagation}return!0},B=function(){var e=!1,t=function(e){var t=e.originalEvent.deltaX,o=-1*e.originalEvent.deltaY;return(t===void 0||o===void 0)&&(t=-1*e.originalEvent.wheelDeltaX/6,o=e.originalEvent.wheelDeltaY/6),e.originalEvent.deltaMode&&1===e.originalEvent.deltaMode&&(t*=10,o*=10),t!==t&&o!==o&&(t=0,o=e.originalEvent.wheelDelta),[t,o]},o=function(o){var n=t(o),r=n[0],c=n[1];e=!1,l.useBothWheelAxes?i&&!s?(c?a.scrollTop(a.scrollTop()-c*l.wheelSpeed):a.scrollTop(a.scrollTop()+r*l.wheelSpeed),e=!0):s&&!i&&(r?a.scrollLeft(a.scrollLeft()+r*l.wheelSpeed):a.scrollLeft(a.scrollLeft()-c*l.wheelSpeed),e=!0):(a.scrollTop(a.scrollTop()-c*l.wheelSpeed),a.scrollLeft(a.scrollLeft()+r*l.wheelSpeed)),j(),e=e||A(r,c),e&&(o.stopPropagation(),o.preventDefault())};window.onwheel!==void 0?a.bind("wheel"+X,o):window.onmousewheel!==void 0&&a.bind("mousewheel"+X,o)},H=function(){var t=!1;a.bind("mouseenter"+X,function(){t=!0}),a.bind("mouseleave"+X,function(){t=!1});var o=!1;e(document).bind("keydown"+X,function(n){if(!(n.isDefaultPrevented&&n.isDefaultPrevented()||!t||e(document.activeElement).is(":input,[contenteditable]"))){var r=0,l=0;switch(n.which){case 37:r=-30;break;case 38:l=30;break;case 39:r=30;break;case 40:l=-30;break;case 33:l=90;break;case 32:case 34:l=-90;break;case 35:l=-d;break;case 36:l=d;break;default:return}a.scrollTop(a.scrollTop()-l),a.scrollLeft(a.scrollLeft()+r),o=A(r,l),o&&n.preventDefault()}})},K=function(){var e=function(e){e.stopPropagation()};T.bind("click"+X,e),m.bind("click"+X,function(e){var t=parseInt(h/2,10),o=e.pageY-m.offset().top-t,n=d-h,r=o/n;0>r?r=0:r>1&&(r=1),a.scrollTop((p-d)*r)}),w.bind("click"+X,e),g.bind("click"+X,function(e){var t=parseInt(f/2,10),o=e.pageX-g.offset().left-t,n=c-f,r=o/n;0>r?r=0:r>1&&(r=1),a.scrollLeft((u-c)*r)})},Q=function(){var t=function(e,t){a.scrollTop(a.scrollTop()-t),a.scrollLeft(a.scrollLeft()-e),j()},o={},n=0,r={},l=null,s=!1;e(window).bind("touchstart"+X,function(){s=!0}),e(window).bind("touchend"+X,function(){s=!1}),a.bind("touchstart"+X,function(e){var t=e.originalEvent.targetTouches[0];o.pageX=t.pageX,o.pageY=t.pageY,n=(new Date).getTime(),null!==l&&clearInterval(l),e.stopPropagation()}),a.bind("touchmove"+X,function(e){if(!s&&1===e.originalEvent.targetTouches.length){var l=e.originalEvent.targetTouches[0],a={};a.pageX=l.pageX,a.pageY=l.pageY;var i=a.pageX-o.pageX,c=a.pageY-o.pageY;t(i,c),o=a;var d=(new Date).getTime(),u=d-n;u>0&&(r.x=i/u,r.y=c/u,n=d),e.preventDefault()}}),a.bind("touchend"+X,function(){clearInterval(l),l=setInterval(function(){return.01>Math.abs(r.x)&&.01>Math.abs(r.y)?(clearInterval(l),void 0):(t(30*r.x,30*r.y),r.x*=.8,r.y*=.8,void 0)},10)})},R=function(){a.bind("scroll"+X,function(){j()})},z=function(){a.unbind(X),e(window).unbind(X),e(document).unbind(X),a.data("perfect-scrollbar",null),a.data("perfect-scrollbar-update",null),a.data("perfect-scrollbar-destroy",null),w.remove(),T.remove(),g.remove(),m.remove(),g=m=w=T=s=i=c=d=u=p=f=v=L=y=I=h=b=S=C=x=D=X=null},F=function(t){a.addClass("ie").addClass("ie"+t);var o=function(){var t=function(){e(this).addClass("hover")},o=function(){e(this).removeClass("hover")};a.bind("mouseenter"+X,t).bind("mouseleave"+X,o),g.bind("mouseenter"+X,t).bind("mouseleave"+X,o),m.bind("mouseenter"+X,t).bind("mouseleave"+X,o),w.bind("mouseenter"+X,t).bind("mouseleave"+X,o),T.bind("mouseenter"+X,t).bind("mouseleave"+X,o)},n=function(){W=function(){var e={left:v+a.scrollLeft(),width:f};y?e.bottom=L:e.top=I,w.css(e);var t={top:b+a.scrollTop(),height:h};C?t.right=S:t.left=x,T.css(t),w.hide().show(),T.hide().show()}};6===t&&(o(),n())},G="ontouchstart"in window||window.DocumentTouch&&document instanceof window.DocumentTouch,J=function(){var e=navigator.userAgent.toLowerCase().match(/(msie) ([\w.]+)/);e&&"msie"===e[1]&&F(parseInt(e[2],10)),j(),R(),O(),q(),K(),B(),G&&Q(),l.useKeyboard&&H(),a.data("perfect-scrollbar",a),a.data("perfect-scrollbar-update",j),a.data("perfect-scrollbar-destroy",z)};return J(),a})}});


/*!
 * hoverIntent v1.8.0 // 2014.06.29 // jQuery v1.9.1+
 * http://cherne.net/brian/resources/jquery.hoverIntent.html
 *
 * You may use hoverIntent under the terms of the MIT license. Basically that
 * means you are free to use hoverIntent as long as this header is left intact.
 * Copyright 2007, 2014 Brian Cherne
 */
(function($){$.fn.hoverIntent=function(handlerIn,handlerOut,selector){var cfg={interval:100,sensitivity:6,timeout:0};if(typeof handlerIn==="object"){cfg=$.extend(cfg,handlerIn)}else{if($.isFunction(handlerOut)){cfg=$.extend(cfg,{over:handlerIn,out:handlerOut,selector:selector})}else{cfg=$.extend(cfg,{over:handlerIn,out:handlerIn,selector:handlerOut})}}var cX,cY,pX,pY;var track=function(ev){cX=ev.pageX;cY=ev.pageY};var compare=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);if(Math.sqrt((pX-cX)*(pX-cX)+(pY-cY)*(pY-cY))<cfg.sensitivity){$(ob).off("mousemove.hoverIntent",track);ob.hoverIntent_s=true;return cfg.over.apply(ob,[ev])}else{pX=cX;pY=cY;ob.hoverIntent_t=setTimeout(function(){compare(ev,ob)},cfg.interval)}};var delay=function(ev,ob){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t);ob.hoverIntent_s=false;return cfg.out.apply(ob,[ev])};var handleHover=function(e){var ev=$.extend({},e);var ob=this;if(ob.hoverIntent_t){ob.hoverIntent_t=clearTimeout(ob.hoverIntent_t)}if(e.type==="mouseenter"){pX=ev.pageX;pY=ev.pageY;$(ob).on("mousemove.hoverIntent",track);if(!ob.hoverIntent_s){ob.hoverIntent_t=setTimeout(function(){compare(ev,ob)},cfg.interval)}}else{$(ob).off("mousemove.hoverIntent",track);if(ob.hoverIntent_s){ob.hoverIntent_t=setTimeout(function(){delay(ev,ob)},cfg.timeout)}}};return this.on({"mouseenter.hoverIntent":handleHover,"mouseleave.hoverIntent":handleHover},cfg.selector)}})(jQuery);


/*! Cookies.js - 0.4.0; Copyright (c) 2014, Scott Hamper; http://www.opensource.org/licenses/MIT */
(function(e){"use strict";var b=function(a,d,c){return 1===arguments.length?b.get(a):b.set(a,d,c)};b._document=document;b._navigator=navigator;b.defaults={path:"/"};b.get=function(a){b._cachedDocumentCookie!==b._document.cookie&&b._renewCache();return b._cache[a]};b.set=function(a,d,c){c=b._getExtendedOptions(c);c.expires=b._getExpiresDate(d===e?-1:c.expires);b._document.cookie=b._generateCookieString(a,d,c);return b};b.expire=function(a,d){return b.set(a,e,d)};b._getExtendedOptions=function(a){return{path:a&& a.path||b.defaults.path,domain:a&&a.domain||b.defaults.domain,expires:a&&a.expires||b.defaults.expires,secure:a&&a.secure!==e?a.secure:b.defaults.secure}};b._isValidDate=function(a){return"[object Date]"===Object.prototype.toString.call(a)&&!isNaN(a.getTime())};b._getExpiresDate=function(a,d){d=d||new Date;switch(typeof a){case "number":a=new Date(d.getTime()+1E3*a);break;case "string":a=new Date(a)}if(a&&!b._isValidDate(a))throw Error("`expires` parameter cannot be converted to a valid Date instance"); return a};b._generateCookieString=function(a,b,c){a=a.replace(/[^#$&+\^`|]/g,encodeURIComponent);a=a.replace(/\(/g,"%28").replace(/\)/g,"%29");b=(b+"").replace(/[^!#$&-+\--:<-\[\]-~]/g,encodeURIComponent);c=c||{};a=a+"="+b+(c.path?";path="+c.path:"");a+=c.domain?";domain="+c.domain:"";a+=c.expires?";expires="+c.expires.toUTCString():"";return a+=c.secure?";secure":""};b._getCookieObjectFromString=function(a){var d={};a=a?a.split("; "):[];for(var c=0;c<a.length;c++){var f=b._getKeyValuePairFromCookieString(a[c]); d[f.key]===e&&(d[f.key]=f.value)}return d};b._getKeyValuePairFromCookieString=function(a){var b=a.indexOf("="),b=0>b?a.length:b;return{key:decodeURIComponent(a.substr(0,b)),value:decodeURIComponent(a.substr(b+1))}};b._renewCache=function(){b._cache=b._getCookieObjectFromString(b._document.cookie);b._cachedDocumentCookie=b._document.cookie};b._areEnabled=function(){var a="1"===b.set("cookies.js",1).get("cookies.js");b.expire("cookies.js");return a};b.enabled=b._areEnabled();"function"===typeof define&& define.amd?define(function(){return b}):"undefined"!==typeof exports?("undefined"!==typeof module&&module.exports&&(exports=module.exports=b),exports.Cookies=b):window.Cookies=b})();








/*
	This function will be called in the event when browser breakpoint changes
 */

var public_vars = public_vars || {};

jQuery.extend(public_vars, {

    breakpoints: {
        largescreen: 	[991, -1],
        tabletscreen: 	[768, 990],
        devicescreen: 	[420, 767],
        sdevicescreen:	[0, 419]
    },

    lastBreakpoint: null
});


/* Main Function that will be called each time when the screen breakpoint changes */
function resizable(breakpoint)
{
    var sb_with_animation;

    // Large Screen Specific Script
    if(is('largescreen'))
    {

    }


    // Tablet or larger screen
    if(ismdxl())
    {
    }


    // Tablet Screen Specific Script
    if(is('tabletscreen'))
    {
    }


    // Tablet device screen
    if(is('tabletscreen'))
    {
        public_vars.$sidebarMenu.addClass('collapsed');
        ps_destroy();
    }


    // Tablet Screen Specific Script
    if(isxs())
    {
    }


    // Trigger Event
    jQuery(window).trigger('xenon.resize');
}



/* Functions */

// Get current breakpoint
function get_current_breakpoint()
{
    var width = jQuery(window).width(),
        breakpoints = public_vars.breakpoints;

    for(var breakpont_label in breakpoints)
    {
        var bp_arr = breakpoints[breakpont_label],
            min = bp_arr[0],
            max = bp_arr[1];

        if(max == -1)
            max = width;

        if(min <= width && max >= width)
        {
            return breakpont_label;
        }
    }

    return null;
}


// Check current screen breakpoint
function is(screen_label)
{
    return get_current_breakpoint() == screen_label;
}


// Is xs device
function isxs()
{
    return is('devicescreen') || is('sdevicescreen');
}

// Is md or xl
function ismdxl()
{
    return is('tabletscreen') || is('largescreen');
}


// Trigger Resizable Function
function trigger_resizable()
{
    if(public_vars.lastBreakpoint != get_current_breakpoint())
    {
        public_vars.lastBreakpoint = get_current_breakpoint();
        resizable(public_vars.lastBreakpoint);
    }


    // Trigger Event (Repeated)
    jQuery(window).trigger('xenon.resized');
}