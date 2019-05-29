class Config(object):
	"""

	common configuartion

	"""

class DevelopmentConfig(Config):
	"""
	Development mode configuration
	"""
	DEBUG = True
	SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
	"""
	Production mode configuration
	"""
	DEBUG = False

app_config = {
	'development': DevelopmentConfig,
	'production': ProductionConfig
}



