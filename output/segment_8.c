 * @delay_buf:		data acquisition intervals table
 * @batch_latency_buf:	yet unknown but existing in communication protocol
 * @batch_opt_buf:	yet unknown but existing in communication protocol
 * @accel_position:	yet unknown but existing in communication protocol
 * @mag_position:	yet unknown but existing in communication protocol
 * @fw_dl_state:	firmware download state
 * @comm_lock:		lock protecting the handshake
 * @pending_lock:	lock protecting pending list and completion
 * @mcu_reset_gpiod:	mcu reset line
 * @ap_mcu_gpiod:	ap to mcu gpio line
 * @mcu_ap_gpiod:	mcu to ap gpio line
 * @pending_list:	pending list for messages queued to be sent/read
 * @sensor_devs:	registered IIO devices table
 * @enable_refcount:	enable reference count for wdt (watchdog timer)
 * @header_buffer:	cache aligned buffer for packet header
 */












};



			 u8 *send_buf, u8 length);







#endif /* __SSP_SENSORHUB_H__ */