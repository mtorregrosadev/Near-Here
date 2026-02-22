"""
AppCtx - Shared application context passed to all page builders.
Holds mutable state, UI component references, and callbacks so they
can be accessed from separate page modules without using global variables.
"""


class AppCtx:
    def __init__(self, APP_SESSIONS, get_client_storage, logger):
        self.APP_SESSIONS = APP_SESSIONS
        self.get_client_storage = get_client_storage
        self.logger = logger

        # ── Mutable flags ──────────────────────────────────────────────
        self.canvi = False          # True when search params changed
        self.ai = 0                 # AI overlay state (0=off, 2=on)
        self.sostenible = True
        self.sostenible_2 = True
        self.Yelp = False
        self.Foursquare = False
        self.Sostenible_L = False
        self.index_photo_stack = -1
        self.index_photo = 0

        # ── UI Components (assigned after creation in main()) ───────────
        self.cards = []
        self.stack_cards = None
        self.botons = None
        self.Tags_amunt = None
        self.images_saved = None
        self.configuracio = None
        self.size_botons = 14.0

        # ── Domain data ─────────────────────────────────────────────────
        self.categories_list: dict = {}

        # ── Callbacks (assigned after function definitions in main()) ───
        self.categ_check_sel = None
        self.categ_chip_sel = None
        self.view_pop = None
        self.seguent = None
        self.guarda = None
        self.mes_info = None
        self.config_nav = None      # "Obre configuració" in error page
        self.update_cards = None
        self.scale_next_card = None
        self.mes_info_select = None
        self.gl = None              # Geolocator instance
