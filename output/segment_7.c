#endif

/* Sensor polling in ms */

};

};

/* Firmware download STATE */
};


/* AP -> SSP Instruction */




/* voice data */

/* Factory Test */

/* SSP -> AP ACK about write CMD */

};

/* ssp_msg options bit */


/**
 * struct ssp_data - ssp platformdata structure
 * @spi:		spi device
 * @sensorhub_info:	info about sensorhub board specific features
 * @wdt_timer:		watchdog timer
 * @work_wdt:		watchdog work
 * @work_firmware:	firmware upgrade work queue
 * @work_refresh:	refresh work queue for reset request from MCU
 * @shut_down:		shut down flag
 * @mcu_dump_mode:	mcu dump mode for debug
 * @time_syncing:	time syncing indication flag
 * @timestamp:		previous time in ns calculated for time syncing
 * @check_status:	status table for each sensor
 * @com_fail_cnt:	communication fail count
 * @reset_cnt:		reset count
 * @timeout_cnt:	timeout count
 * @available_sensors:	available sensors seen by sensorhub (bit array)
 * @cur_firm_rev:	cached current firmware revision
 * @last_resume_state:	last AP resume/suspend state used to handle the PM
 *                      state of ssp
 * @last_ap_state:	(obsolete) sleep notification for MCU
 * @sensor_enable:	sensor enable mask
