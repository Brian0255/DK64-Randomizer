"""Options for the main rando tab."""
import random
import re

import js
from js import document
from randomizer.Enums.Items import Items
from randomizer.Enums.Plandomizer import ItemToPlandoItemMap, PlandoItems
from randomizer.Enums.Settings import SettingsMap
from randomizer.Lists.Item import StartingMoveOptions
from randomizer.Lists.Songs import MusicSelectionPanel
from randomizer.PlandoUtils import MoveSet
from randomizer.SettingStrings import decrypt_settings_string_enum
from ui.bindings import bind, bindList
from ui.randomize_settings import randomize_settings


def randomseed(evt):
    """Randomly generate a seed ID."""
    document.getElementById("seed").value = str(random.randint(100000, 999999))


@bind("input", "blocker_", 8)
@bind("input", "troff_", 8)
@bind("input", "blocker_text")
@bind("input", "troff_text")
def on_input(event):
    """Limits inputs from input boxes on keypress.

    Args:
        event (domevent): The DOMEvent data.

    Returns:
        bool: False if we need to stop the event.
    """
    # Make sure we limit the max items in each of these text boxes values
    if event.target.id == "blocker_text":
        return
    elif event.target.id == "troff_text":
        return
    elif "troff" in event.target.id:
        min_max(event, 0, 500)
    elif "blocker" in event.target.id:
        min_max(event, 0, 200)


@bind("focusout", "progressive_hint_text")
def handle_progressive_hint_text(event):
    """Validate blocker input on loss of focus."""
    progressive_hint_text = js.document.getElementById("progressive_hint_text")
    if not progressive_hint_text.value:
        progressive_hint_text.value = 60
    elif int(progressive_hint_text.value) < 1:
        progressive_hint_text.value = 1
    elif int(progressive_hint_text.value) > 201:
        progressive_hint_text.value = 201


@bind("focusout", "blocker_text")
def max_randomized_blocker(event):
    """Validate blocker input on loss of focus."""
    blocker_text = js.document.getElementById("blocker_text")
    if not blocker_text.value:
        blocker_text.value = 50
    elif 0 <= int(blocker_text.value) < 8:
        blocker_text.value = 8
    elif int(blocker_text.value) > 200:
        blocker_text.value = 200


@bind("focusout", "troff_text")
def max_randomized_troff(event):
    """Validate troff input on loss of focus."""
    troff_text = js.document.getElementById("troff_text")
    if not troff_text.value:
        troff_text.value = 300
    elif int(troff_text.value) > 500:
        troff_text.value = 500


@bind("focusout", "music_volume")
def max_music(event):
    """Validate music input on loss of focus."""
    music_text = js.document.getElementById("music_volume")
    if not music_text.value:
        music_text.value = 100
    elif int(music_text.value) > 100:
        music_text.value = 100
    elif int(music_text.value) < 0:
        music_text.value = 0


@bind("focusout", "custom_music_proportion")
def max_music_proportion(event):
    """Validate music input on loss of focus."""
    music_text = js.document.getElementById("custom_music_proportion")
    if not music_text.value:
        music_text.value = 100
    elif int(music_text.value) > 100:
        music_text.value = 100
    elif int(music_text.value) < 0:
        music_text.value = 0


@bind("focusout", "sfx_volume")
def max_sfx(event):
    """Validate sfx input on loss of focus."""
    sfx_text = js.document.getElementById("sfx_volume")
    if not sfx_text.value:
        sfx_text.value = 100
    elif int(sfx_text.value) > 100:
        sfx_text.value = 100
    elif int(sfx_text.value) < 0:
        sfx_text.value = 0


@bind("focusout", "medal_requirement")
def max_randomized_medals(event):
    """Validate medal input on loss of focus."""
    medal_requirement = js.document.getElementById("medal_requirement")
    if not medal_requirement.value:
        medal_requirement.value = 15
    elif 0 > int(medal_requirement.value):
        medal_requirement.value = 0
    elif int(medal_requirement.value) > 40:
        medal_requirement.value = 40


@bind("focusout", "medal_cb_req")
def max_randomized_medal_cb_req(event):
    """Validate cb medal input on loss of focus."""
    medal_cb_req = js.document.getElementById("medal_cb_req")
    if not medal_cb_req.value:
        medal_cb_req.value = 75
    elif 1 > int(medal_cb_req.value):
        medal_cb_req.value = 1
    elif int(medal_cb_req.value) > 100:
        medal_cb_req.value = 100


@bind("focusout", "rareware_gb_fairies")
def max_randomized_fairies(event):
    """Validate fairy input on loss of focus."""
    fairy_req = js.document.getElementById("rareware_gb_fairies")
    if not fairy_req.value:
        fairy_req.value = 20
    elif 1 > int(fairy_req.value):
        fairy_req.value = 1
    elif int(fairy_req.value) > 20:
        fairy_req.value = 20


@bind("click", "shuffle_items")
@bind("change", "move_rando")
@bind("focusout", "starting_moves_count")
def max_starting_moves_count(event):
    """Validate starting moves count input on loss of focus."""
    move_count = js.document.getElementById("starting_moves_count")
    moves = js.document.getElementById("move_rando")
    item_rando = js.document.getElementById("shuffle_items")
    max_starting_moves = 40
    if not item_rando.checked and moves.value != "off":
        max_starting_moves = 4
    if not move_count.value:
        move_count.value = 4
    elif 0 > int(move_count.value):
        move_count.value = 0
    elif int(move_count.value) > max_starting_moves:
        move_count.value = max_starting_moves


@bind("change", "crown_door_item")
def updateDoorOneNumAccess(event):
    """Toggle the textboxes for the first helm door."""
    door_one_selection = js.document.getElementById("crown_door_item")
    disabled = (door_one_selection.value == "random") or (door_one_selection.value == "opened")
    door_one_req = js.document.getElementById("crown_door_item_count")
    if disabled:
        door_one_req.setAttribute("disabled", "disabled")
    else:
        door_one_req.removeAttribute("disabled")
    if not door_one_req.value:
        door_one_req.value = 1
    elif door_one_selection.value == "vanilla" and int(door_one_req.value) > 10:
        door_one_req.value = 10
    elif door_one_selection.value == "req_gb" and int(door_one_req.value) > 201:
        door_one_req.value = 201
    elif door_one_selection.value == "req_bp" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_medal" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_companycoins" and int(door_one_req.value) > 2:
        door_one_req.value = 2
    elif door_one_selection.value == "req_key" and int(door_one_req.value) > 8:
        door_one_req.value = 8
    elif door_one_selection.value == "req_fairy" and int(door_one_req.value) > 18:
        door_one_req.value = 18
    elif door_one_selection.value == "req_bean" and int(door_one_req.value) > 1:
        door_one_req.value = 1
    elif door_one_selection.value == "req_pearl" and int(door_one_req.value) > 5:
        door_one_req.value = 5
    elif door_one_selection.value == "req_rainbowcoin" and int(door_one_req.value) > 16:
        door_one_req.value = 16


@bind("click", "nav-progression-tab")
@bind("change", "crown_door_item")
def updateDoorOneCountText(evt):
    """Change the text of the door 1 item count label."""
    label_text_map = {
        "vanilla": "Crowns",
        "req_gb": "Bananas",
        "req_bp": "Blueprints",
        "req_companycoins": "Coins",
        "req_key": "Keys",
        "req_medal": "Medals",
        "req_fairy": "Fairies",
        "req_rainbowcoin": "Coins",
        "req_bean": "Bean",
        "req_pearl": "Pearls",
    }
    door_one_text = js.document.getElementById("door-1-select-title")
    door_one_selection = js.document.getElementById("crown_door_item").value
    if door_one_selection in label_text_map:
        door_one_text.innerText = f"{label_text_map[door_one_selection]} Needed For Door 1"
    else:
        door_one_text.innerText = "Door 1 Item Count"


@bind("change", "coin_door_item")
def updateDoorTwoNumAccess(event):
    """Toggle the textboxes for the second helm door."""
    door_two_selection = js.document.getElementById("coin_door_item")
    disabled = (door_two_selection.value == "random") or (door_two_selection.value == "opened")
    door_two_req = js.document.getElementById("coin_door_item_count")
    if disabled:
        door_two_req.setAttribute("disabled", "disabled")
    else:
        door_two_req.removeAttribute("disabled")
    if not door_two_req.value:
        door_two_req.value = 1
    elif door_two_selection.value == "vanilla" and int(door_two_req.value) > 2:
        door_two_req.value = 2
    elif door_two_selection.value == "req_gb" and int(door_two_req.value) > 201:
        door_two_req.value = 201
    elif door_two_selection.value == "req_bp" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_key" and int(door_two_req.value) > 8:
        door_two_req.value = 8
    elif door_two_selection.value == "req_medal" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_crown" and int(door_two_req.value) > 10:
        door_two_req.value = 10
    elif door_two_selection.value == "req_fairy" and int(door_two_req.value) > 18:
        door_two_req.value = 18
    elif door_two_selection.value == "req_bean" and int(door_two_req.value) > 1:
        door_two_req.value = 1
    elif door_two_selection.value == "req_pearl" and int(door_two_req.value) > 5:
        door_two_req.value = 5
    elif door_two_selection.value == "req_rainbowcoin" and int(door_two_req.value) > 16:
        door_two_req.value = 16


@bind("click", "nav-progression-tab")
@bind("change", "coin_door_item")
def updateDoorTwoCountText(evt):
    """Change the text of the door 2 item count label."""
    label_text_map = {
        "vanilla": "Coins",
        "req_gb": "Bananas",
        "req_bp": "Blueprints",
        "req_key": "Keys",
        "req_medal": "Medals",
        "req_crown": "Crowns",
        "req_fairy": "Fairies",
        "req_rainbowcoin": "Coins",
        "req_bean": "Bean",
        "req_pearl": "Pearls",
    }
    door_two_text = js.document.getElementById("door-2-select-title")
    door_two_selection = js.document.getElementById("coin_door_item").value
    if door_two_selection in label_text_map:
        door_two_text.innerText = f"{label_text_map[door_two_selection]} Needed For Door 2"
    else:
        door_two_text.innerText = "Door 2 Item Count"


@bind("focusout", "crown_door_item_count")
def max_doorone_requirement(event):
    """Validate Door 1 input on loss of focus."""
    door_one_req = js.document.getElementById("crown_door_item_count")
    door_one_selection = js.document.getElementById("crown_door_item")
    # Never go below 1 for any option
    if not door_one_req.value:
        door_one_req.value = 1
    elif 1 > int(door_one_req.value):
        door_one_req.value = 1
    if door_one_selection.value == "vanilla" and int(door_one_req.value) > 10:
        door_one_req.value = 10
    elif door_one_selection.value == "req_gb" and int(door_one_req.value) > 201:
        door_one_req.value = 201
    elif door_one_selection.value == "req_bp" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_companycoins" and int(door_one_req.value) > 2:
        door_one_req.value = 2
    elif door_one_selection.value == "req_key" and int(door_one_req.value) > 8:
        door_one_req.value = 8
    elif door_one_selection.value == "req_medal" and int(door_one_req.value) > 40:
        door_one_req.value = 40
    elif door_one_selection.value == "req_fairy" and int(door_one_req.value) > 18:
        door_one_req.value = 18
    elif door_one_selection.value == "req_bean" and int(door_one_req.value) > 1:
        door_one_req.value = 1
    elif door_one_selection.value == "req_pearl" and int(door_one_req.value) > 5:
        door_one_req.value = 5


@bind("focusout", "coin_door_item_count")
def max_doortwo_requirement(event):
    """Validate Door 2 input on loss of focus."""
    door_two_req = js.document.getElementById("coin_door_item_count")
    door_two_selection = js.document.getElementById("coin_door_item")
    if not door_two_req.value:
        door_two_req.value = 1
    elif 1 > int(door_two_req.value):
        door_two_req.value = 1
    if door_two_selection.value == "vanilla" and int(door_two_req.value) > 2:
        door_two_req.value = 2
    elif door_two_selection.value == "req_gb" and int(door_two_req.value) > 201:
        door_two_req.value = 201
    elif door_two_selection.value == "req_bp" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_key" and int(door_two_req.value) > 8:
        door_two_req.value = 8
    elif door_two_selection.value == "req_medal" and int(door_two_req.value) > 40:
        door_two_req.value = 40
    elif door_two_selection.value == "req_crown" and int(door_two_req.value) > 10:
        door_two_req.value = 10
    elif door_two_selection.value == "req_fairy" and int(door_two_req.value) > 18:
        door_two_req.value = 18
    elif door_two_selection.value == "req_bean" and int(door_two_req.value) > 1:
        door_two_req.value = 1
    elif door_two_selection.value == "req_pearl" and int(door_two_req.value) > 5:
        door_two_req.value = 5


def min_max(event, min, max):
    """Check if the data is within bounds of requirements.

    Args:
        event (DomEvent): The doms event.
        min (int): Minimum Value to keep.
        max (int): Maximum value to allow.

    Returns:
        bool: Deny or Success for Handled
    """
    try:
        # Attempt to cap our min and max for events on numbers
        if int(event.target.value) >= max:
            event.preventDefault()
            document.getElementById(event.target.id).value = max
        elif int(event.target.value) <= min:
            event.preventDefault()
            document.getElementById(event.target.id).value = min
        else:
            document.getElementById(event.target.id).value = str(event.target.value)
    except Exception:
        # Set the value to min if something goes wrong
        event.preventDefault()
        document.getElementById(event.target.id).value = min


@bind("keydown", "blocker_", 8)
@bind("keydown", "troff_", 8)
@bind("keydown", "blocker_text")
@bind("keydown", "troff_text")
def key_down(event):
    """Check if a key is a proper number, deletion, navigation, Copy/Cut/Paste.

    Args:
        event (DomEvent): Event from the DOM.
    """
    # Disable all buttons that are not in the list below or a digit
    global_keys = ["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Control_L", "Control_R", "x", "v", "c"]
    if not event.key.isdigit() and event.key not in global_keys:
        event.preventDefault()
    else:
        pass


def set_random_weights_options():
    """Set the random settings presets on the page."""
    element = document.getElementById("random-weights")
    children = []
    # Take note of the items currently in the dropdown.
    for child in element.children:
        children.append(child.value)
    # Add all of the random weights presets.
    for val in js.random_settings_presets:
        if val.get("name") not in children:
            opt = document.createElement("option")
            opt.value = val.get("name")
            opt.innerHTML = val.get("name")
            opt.title = val.get("description")
            element.appendChild(opt)
            if val.get("name") == "Standard":
                opt.selected = True


def set_preset_options():
    """Set the Blocker presets on the page."""
    # Check what the selected dropdown item is
    element = document.getElementById("presets")
    children = []
    # Find all the items in the dropdown
    for child in element.children:
        children.append(child.value)
    # Find out dropdown item and set our selected item text to it
    for val in js.progression_presets:
        if val.get("name") not in children:
            opt = document.createElement("option")
            opt.value = val.get("name")
            opt.innerHTML = val.get("name")
            opt.title = val.get("description")
            element.appendChild(opt)
            if val.get("name") == "-- Select a Preset --":
                opt.disabled = True
                opt.hidden = True
    js.jq("#presets").val("-- Select a Preset --")
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    toggle_logic_type(None)
    toggle_bananaport_selector(None)
    updateDoorOneNumAccess(None)
    updateDoorTwoNumAccess(None)

    js.load_data()


@bind("click", "randomize_blocker_required_amounts")
def toggle_b_locker_boxes(event):
    """Toggle the textboxes for BLockers."""
    disabled = True
    if js.document.getElementById("randomize_blocker_required_amounts").checked:
        disabled = False
    blocker_text = js.document.getElementById("blocker_text")
    maximize_helm_blocker = js.document.getElementById("maximize_helm_blocker")
    if disabled:
        blocker_text.setAttribute("disabled", "disabled")
        maximize_helm_blocker.setAttribute("disabled", "disabled")
    else:
        blocker_text.removeAttribute("disabled")
        maximize_helm_blocker.removeAttribute("disabled")
    for i in range(0, 10):
        blocker = js.document.getElementById(f"blocker_{i}")
        try:
            if disabled:
                blocker.removeAttribute("disabled")
            else:
                blocker.setAttribute("disabled", "disabled")
        except AttributeError:
            pass


@bind("click", "randomize_cb_required_amounts")
def toggle_counts_boxes(event):
    """Toggle the textboxes for Troff."""
    disabled = True
    if js.document.getElementById("randomize_cb_required_amounts").checked:
        disabled = False
    troff_text = js.document.getElementById("troff_text")
    if disabled:
        troff_text.setAttribute("disabled", "disabled")
    else:
        troff_text.removeAttribute("disabled")
    for i in range(0, 10):
        troff = js.document.getElementById(f"troff_{i}")
        try:
            if disabled:
                troff.removeAttribute("disabled")
            else:
                troff.setAttribute("disabled", "disabled")
        except AttributeError:
            pass


@bind("change", "level_randomization")
def update_boss_required(evt):
    """Disable certain page flags depending on checkboxes."""
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    moves = document.getElementById("move_off")
    hard_level_progression = document.getElementById("hard_level_progression")
    if level.value == "level_order":
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        kong_rando.setAttribute("disabled", "disabled")
        kong_rando.checked = True
        if moves.selected is True:
            document.getElementById("move_on").selected = True
        moves.setAttribute("disabled", "disabled")
        hard_level_progression.removeAttribute("disabled")
    elif level.value == "vanilla" and kong_rando.checked:
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
        kong_rando.removeAttribute("disabled")
        moves.removeAttribute("disabled")
        hard_level_progression.setAttribute("disabled", "disabled")
        hard_level_progression.checked = False
    else:
        try:
            boss_kong.removeAttribute("disabled")
            boss_location.removeAttribute("disabled")
            kong_rando.removeAttribute("disabled")
            moves.removeAttribute("disabled")
            hard_level_progression.setAttribute("disabled", "disabled")
            hard_level_progression.checked = False
        except Exception:
            pass


@bind("click", "kong_rando")
def disable_boss_rando(evt):
    """Disable Boss Kong and Boss Location Rando if Vanilla levels and Kong Rando."""
    level = document.getElementById("level_randomization")
    boss_location = document.getElementById("boss_location_rando")
    boss_kong = document.getElementById("boss_kong_rando")
    kong_rando = document.getElementById("kong_rando")
    if kong_rando.checked and level.value == "vanilla" or level.value == "level_order":
        boss_location.setAttribute("disabled", "disabled")
        boss_location.checked = True
        boss_kong.setAttribute("disabled", "disabled")
        boss_kong.checked = True
    else:
        boss_kong.removeAttribute("disabled")
        boss_location.removeAttribute("disabled")
        kong_rando.removeAttribute("disabled")


@bind("click", "random_colors")
def disable_colors(evt):
    """Disable color options when Randomize All is selected."""
    disabled = False
    if js.document.getElementById("random_colors").checked:
        disabled = True
    for i in ["dk", "diddy", "tiny", "lanky", "chunky", "rambi", "enguarde"]:
        color = js.document.getElementById(f"{i}_colors")
        try:
            if disabled:
                color.setAttribute("disabled", "disabled")
            else:
                color.removeAttribute("disabled")
        except AttributeError:
            pass
    hide_rgb(None)


@bind("click", "enable_tag_anywhere")
def disable_tag_spawn(evt):
    """Disable 'Disable Tag Spawn' option when 'Tag Anywhere' is off."""
    disabled = False
    if js.document.getElementById("enable_tag_anywhere").checked is False:
        disabled = True
    if disabled:
        js.document.getElementById("disable_tag_barrels").setAttribute("disabled", "disabled")
        js.document.getElementById("disable_tag_barrels").checked = False
    else:
        js.document.getElementById("disable_tag_barrels").removeAttribute("disabled")


@bind("click", "disable_tag_barrels")
def enable_tag_anywhere(evt):
    """Enable 'Tag Anywhere' if 'Disable Tag Spawn' option is on."""
    if js.document.getElementById("disable_tag_barrels").checked:
        js.document.getElementById("enable_tag_anywhere").checked = True


@bind("click", "random_music")
def disable_music(evt):
    """Disable music options when Randomize All is selected."""
    disabled = False
    if js.document.getElementById("random_music").checked:
        disabled = True
    for i in ["bgm", "majoritems", "minoritems", "events"]:
        music = js.document.getElementById(f"music_{i}_randomized")
        try:
            if disabled:
                music.setAttribute("disabled", "disabled")
                music.setAttribute("checked", "checked")
            else:
                music.removeAttribute("disabled")
        except AttributeError:
            pass


@bind("change", "starting_kongs_count")
def enable_kong_rando(evt):
    """Enable Kong Rando if less than 5 starting kongs."""
    kong_rando = js.document.getElementById("kong_rando")
    if js.document.getElementById("starting_kongs_count").value == "5":
        kong_rando.checked = False
        kong_rando.setAttribute("disabled", "disabled")
    else:
        kong_rando.removeAttribute("disabled")


@bind("click", "krool_random")
def disable_krool_phases(evt):
    """Disable K Rool options when Randomize All is selected."""
    disabled = False
    krool = js.document.getElementById("krool_phase_count")
    if js.document.getElementById("krool_random").checked:
        disabled = True
    try:
        if disabled:
            krool.setAttribute("disabled", "disabled")
        else:
            krool.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "helm_random")
def disable_helm_phases(evt):
    """Disable Helm options when Randomize All is selected."""
    disabled = False
    helm = js.document.getElementById("helm_phase_count")
    if js.document.getElementById("helm_random").checked:
        disabled = True
    try:
        if disabled:
            helm.setAttribute("disabled", "disabled")
        else:
            helm.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "krool_random")
@bind("change", "krool_phase_count")
def plando_hide_krool_options(evt):
    """Hide the plando options to select Kongs for certain K. Rool phases if those phases are disabled."""
    krool_phase_count = int(js.document.getElementById("krool_phase_count").value)
    krool_random = js.document.getElementById("krool_random").checked
    for i in range(0, 5):
        krool_phase_plando_div = js.document.getElementById(f"plando_krool_order_div_{i}")
        krool_phase_plando = js.document.getElementById(f"plando_krool_order_{i}")
        if i < krool_phase_count or krool_random:
            krool_phase_plando_div.classList.remove("disabled-select")
            krool_phase_plando.removeAttribute("disabled")
        else:
            krool_phase_plando_div.classList.add("disabled-select")
            krool_phase_plando.setAttribute("disabled", "disabled")
            krool_phase_plando.value = ""


@bind("click", "helm_random")
@bind("change", "helm_phase_count")
def plando_hide_helm_options(evt):
    """Hide the plando options to select Kongs for certain Helm phases if those phases are disabled."""
    helm_phase_count = int(js.document.getElementById("helm_phase_count").value)
    helm_random = js.document.getElementById("helm_random").checked
    for i in range(0, 5):
        helm_phase_plando_div = js.document.getElementById(f"plando_helm_order_div_{i}")
        helm_phase_plando = js.document.getElementById(f"plando_helm_order_{i}")
        if i < helm_phase_count or helm_random:
            helm_phase_plando_div.classList.remove("disabled-select")
            helm_phase_plando.removeAttribute("disabled")
        else:
            helm_phase_plando_div.classList.add("disabled-select")
            helm_phase_plando.setAttribute("disabled", "disabled")
            helm_phase_plando.value = ""


@bind("click", "nav-plando-tab")
def plando_propagate_options(evt):
    """Make changes to the plando tab based on other settings.

    This is partly a workaround for issues with the Bootstrap slider.
    """
    plando_hide_krool_options(evt)
    plando_hide_helm_options(evt)
    plando_disable_camera_shockwave(evt)


@bind("change", "move_rando")
def disable_move_shuffles(evt):
    """Disable some settings based on the move rando setting."""
    moves = js.document.getElementById("move_rando")
    prices = js.document.getElementById("random_prices")
    training_barrels = js.document.getElementById("training_barrels")
    shockwave_status = js.document.getElementById("shockwave_status")
    starting_moves_count = js.document.getElementById("starting_moves_count")
    start_with_slam = js.document.getElementById("start_with_slam")
    try:
        if moves.value == "start_with":
            prices.setAttribute("disabled", "disabled")
            training_barrels.value = "normal"
            training_barrels.setAttribute("disabled", "disabled")
            shockwave_status.value = "vanilla"
            shockwave_status.setAttribute("disabled", "disabled")
            starting_moves_count.value = 40
            starting_moves_count.setAttribute("disabled", "disabled")
            start_with_slam.checked = True
            start_with_slam.setAttribute("disabled", "disabled")
        elif moves.value == "off":
            prices.removeAttribute("disabled")
            training_barrels.value = "normal"
            training_barrels.setAttribute("disabled", "disabled")
            shockwave_status.value = "vanilla"
            shockwave_status.setAttribute("disabled", "disabled")
            starting_moves_count.value = 40
            starting_moves_count.setAttribute("disabled", "disabled")
            start_with_slam.checked = True
            start_with_slam.setAttribute("disabled", "disabled")
        else:
            prices.removeAttribute("disabled")
            training_barrels.removeAttribute("disabled")
            shockwave_status.removeAttribute("disabled")
            starting_moves_count.removeAttribute("disabled")
            start_with_slam.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "bonus_barrel_rando")
def disable_barrel_modal(evt):
    """Disable Minigame Selector when Shuffle Bonus Barrels is off."""
    disabled = True
    selector = js.document.getElementById("minigames_list_modal")
    if js.document.getElementById("bonus_barrel_rando").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "enemy_rando")
def disable_enemy_modal(evt):
    """Disable Enemy Selector when Enemy Rando is off."""
    disabled = True
    selector = js.document.getElementById("enemies_modal")
    if js.document.getElementById("enemy_rando").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "hard_mode")
def disable_hard_mode_modal(evt):
    """Disable Hard Mode Selector when Hard Mode is off."""
    disabled = True
    selector = js.document.getElementById("hard_mode_modal")
    if js.document.getElementById("hard_mode").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "nav-music-tab")
@bind("click", "songs_excluded")
def disable_excluded_songs_modal(evt):
    """Disable Excluded Song Selector when Excluded Songs is off."""
    disabled = True
    selector = js.document.getElementById("excluded_songs_modal")
    if js.document.getElementById("songs_excluded").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "shuffle_items")
def toggle_item_rando(evt):
    """Enable and disable settings based on Item Rando being on/off."""
    disabled = True
    selector = js.document.getElementById("item_rando_list_modal")
    item_rando_pool = document.getElementById("item_rando_list_selected").options
    smaller_shops = document.getElementById("smaller_shops")
    shockwave = document.getElementById("shockwave_status_shuffled")
    move_vanilla = document.getElementById("move_off")
    move_rando = document.getElementById("move_on")
    enemy_drop_rando = document.getElementById("enemy_drop_rando")
    non_item_rando_warning = document.getElementById("non_item_rando_warning")
    shops_in_pool = False
    nothing_selected = True
    for option in item_rando_pool:
        if option.value == "shop":
            if option.selected:
                shops_in_pool = True
                break
        if option.selected:
            nothing_selected = False
    if nothing_selected:
        shops_in_pool = True
    if js.document.getElementById("shuffle_items").checked:
        disabled = False
    try:
        if disabled:
            # Prevent item rando modal from opening, smaller shop setting, and dropsanity setting
            selector.setAttribute("disabled", "disabled")
            smaller_shops.setAttribute("disabled", "disabled")
            smaller_shops.checked = False
            shockwave.removeAttribute("disabled")
            move_vanilla.removeAttribute("disabled")
            move_rando.removeAttribute("disabled")
            enemy_drop_rando.setAttribute("disabled", "disabled")
            enemy_drop_rando.checked = False
            non_item_rando_warning.removeAttribute("hidden")
        else:
            # Enable item rando modal, prevent shockwave/camera coupling, enable dropsanity, and enable smaller shops if it's in the pool
            selector.removeAttribute("disabled")
            enemy_drop_rando.removeAttribute("disabled")
            non_item_rando_warning.setAttribute("hidden", "hidden")
            if shops_in_pool:
                if shockwave.selected is True:
                    document.getElementById("shockwave_status_shuffled_decoupled").selected = True
                if move_vanilla.selected is True or move_rando.selected is True:
                    document.getElementById("move_on_cross_purchase").selected = True
                shockwave.setAttribute("disabled", "disabled")
                move_vanilla.setAttribute("disabled", "disabled")
                move_rando.setAttribute("disabled", "disabled")
                smaller_shops.removeAttribute("disabled")
                # Prevent UI breaking if Vanilla/Unlock All moves was selected before selection Shops in Item Rando
                js.document.getElementById("training_barrels").removeAttribute("disabled")
                js.document.getElementById("shockwave_status").removeAttribute("disabled")
                js.document.getElementById("random_prices").removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "item_rando_list_select_all")
@bind("click", "item_rando_list_reset")
@bind("click", "item_rando_list_selected")
def item_rando_list_changed(evt):
    """Enable and disable settings based on the Item Rando pool changing."""
    item_rando_disabled = True
    item_rando_pool = document.getElementById("item_rando_list_selected").options
    shockwave = document.getElementById("shockwave_status_shuffled")
    smaller_shops = document.getElementById("smaller_shops")
    move_vanilla = document.getElementById("move_off")
    move_rando = document.getElementById("move_on")
    shops_in_pool = False
    nothing_selected = True
    for option in item_rando_pool:
        if option.value == "shop":
            if option.selected:
                shops_in_pool = True
                break
        if option.selected:
            nothing_selected = False
    if nothing_selected:
        shops_in_pool = True
    if js.document.getElementById("shuffle_items").checked:
        item_rando_disabled = False
    if shops_in_pool and not item_rando_disabled:
        # Prevent camera/shockwave from being coupled and enable smaller shops if shops are in the pool
        if shockwave.selected is True:
            document.getElementById("shockwave_status_shuffled_decoupled").selected = True
        if move_vanilla.selected is True or move_rando.selected is True:
            document.getElementById("move_on_cross_purchase").selected = True
        shockwave.setAttribute("disabled", "disabled")
        move_vanilla.setAttribute("disabled", "disabled")
        move_rando.setAttribute("disabled", "disabled")
        smaller_shops.removeAttribute("disabled")
        # Prevent UI breaking if Vanilla/Unlock All moves was selected before selection Shops in Item Rando
        js.document.getElementById("shockwave_status").removeAttribute("disabled")
        js.document.getElementById("random_prices").removeAttribute("disabled")
    else:
        # Enable coupled camera/shockwave and disable smaller shops if shops are not in the pool
        shockwave.removeAttribute("disabled")
        move_vanilla.removeAttribute("disabled")
        move_rando.removeAttribute("disabled")
        smaller_shops.setAttribute("disabled", "disabled")
        smaller_shops.checked = False


@bind("click", "apply_preset")
def preset_select_changed(event):
    """Trigger a change of the form via the JSON templates."""
    element = document.getElementById("presets")
    presets = None
    for val in js.progression_presets:
        if val.get("name") == element.value:
            presets = val
    if presets is not None and "settings_string" in presets:
        # Pass in setting string
        settings = decrypt_settings_string_enum(presets["settings_string"])
        for select in js.document.getElementsByTagName("select"):
            if js.document.querySelector("#nav-cosmetics").contains(select) is False and not select.name.startswith("plando_"):
                select.selectedIndex = -1
        # Uncheck all starting move radio buttons for the import to then set them correctly
        for starting_move_button in [element for element in js.document.getElementsByTagName("input") if element.name.startswith("starting_move_box_")]:
            starting_move_button.checked = False
        js.document.getElementById("presets").selectedIndex = 0
        for key in settings:
            try:
                if type(settings[key]) is bool:
                    if settings[key] is False:
                        js.jq(f"#{key}").checked = False
                        js.document.getElementsByName(key)[0].checked = False
                    else:
                        js.jq(f"#{key}").checked = True
                        js.document.getElementsByName(key)[0].checked = True
                    js.jq(f"#{key}").removeAttr("disabled")
                elif type(settings[key]) is list:
                    if key in ("starting_move_list_selected", "random_starting_move_list_selected"):
                        for item in settings[key]:
                            radio_buttons = js.document.getElementsByName("starting_move_box_" + str(int(item)))
                            if key == "starting_move_list_selected":
                                start_button = [button for button in radio_buttons if button.id.startswith("start")][0]
                                start_button.checked = True
                            else:
                                random_button = [button for button in radio_buttons if button.id.startswith("random")][0]
                                random_button.checked = True
                        continue
                    selector = js.document.getElementById(key)
                    if selector.tagName == "SELECT":
                        for item in settings[key]:
                            for option in selector.options:
                                if option.value == item.name:
                                    option.selected = True
                else:
                    if js.document.getElementsByName(key)[0].hasAttribute("data-slider-value"):
                        js.jq(f"#{key}").slider("setValue", settings[key])
                        js.jq(f"#{key}").slider("enable")
                        js.jq(f"#{key}").parent().find(".slider-disabled").removeClass("slider-disabled")
                    else:
                        selector = js.document.getElementById(key)
                        # If the selector is a select box, set the selectedIndex to the value of the option
                        if selector.tagName == "SELECT":
                            for option in selector.options:
                                if option.value == SettingsMap[key](settings[key]).name:
                                    # Set the value of the select box to the value of the option
                                    option.selected = True
                                    break
                        else:
                            js.jq(f"#{key}").val(settings[key])
                    js.jq(f"#{key}").removeAttr("disabled")
            except Exception as e:
                print(e)
                pass
    else:
        for key in presets:
            try:
                if type(presets[key]) is bool:
                    if presets[key] is False:
                        js.jq(f"#{key}").checked = False
                        js.document.getElementsByName(key)[0].checked = False
                    else:
                        js.jq(f"#{key}").checked = True
                        js.document.getElementsByName(key)[0].checked = True
                    js.jq(f"#{key}").removeAttr("disabled")
                elif type(presets[key]) is list:
                    selector = js.document.getElementById(key)
                    for i in range(0, selector.options.length):
                        selector.item(i).selected = selector.item(i).value in presets[key]
                else:
                    if js.document.getElementsByName(key)[0].hasAttribute("data-slider-value"):
                        js.jq(f"#{key}").slider("setValue", presets[key])
                        js.jq(f"#{key}").slider("enable")
                        js.jq(f"#{key}").parent().find(".slider-disabled").removeClass("slider-disabled")
                    else:
                        js.jq(f"#{key}").val(presets[key])
                    js.jq(f"#{key}").removeAttr("disabled")
            except Exception as e:
                pass
    toggle_counts_boxes(None)
    toggle_b_locker_boxes(None)
    update_boss_required(None)
    disable_colors(None)
    disable_music(None)
    disable_move_shuffles(None)
    max_randomized_blocker(None)
    handle_progressive_hint_text(None)
    max_randomized_troff(None)
    max_music(None)
    max_music_proportion(None)
    max_sfx(None)
    disable_barrel_modal(None)
    item_rando_list_changed(None)
    toggle_item_rando(None)
    disable_enemy_modal(None)
    disable_hard_mode_modal(None)
    disable_excluded_songs_modal(None)
    toggle_bananaport_selector(None)
    disable_helm_hurry(None)
    toggle_logic_type(None)
    toggle_key_settings(None)
    max_starting_moves_count(None)
    js.savesettings()


@bind("click", "enable_plandomizer")
def enable_plandomizer(evt):
    """Enable and disable the Plandomizer tab."""
    disabled = True
    plando_tab = js.document.getElementById("nav-plando-tab")
    if js.document.getElementById("enable_plandomizer").checked:
        disabled = False
    try:
        if disabled:
            plando_tab.style.display = "none"
        else:
            plando_tab.style = ""
    except AttributeError:
        pass


@bind("click", "enable_plandomizer")
def disable_switchsanity_with_plandomizer(evt):
    """Disable Switchsanity if the Plandomizer is being used."""
    disabled = False
    switchsanity = js.document.getElementsByName("switchsanity")[0]
    if js.document.getElementById("enable_plandomizer").checked:
        disabled = True
    try:
        if disabled:
            switchsanity.checked = False
            switchsanity.setAttribute("disabled", "disabled")
        else:
            switchsanity.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("change", "plando_starting_kongs_selected")
def plando_disable_kong_items(evt):
    """Do not allow starting Kongs to be placed as items."""
    starting_kongs = js.document.getElementById("plando_starting_kongs_selected")
    selected_kongs = {x.value for x in starting_kongs.selectedOptions}
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    for kong in ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]:
        if kong.lower() in selected_kongs:
            kong_options = js.document.getElementsByClassName(f"plando-{kong}-option")
            # Disable this Kong as a dropdown option.
            for option in kong_options:
                option.setAttribute("disabled", "disabled")
            # De-select this Kong everywhere they are selected.
            for dropdown in item_dropdowns:
                if dropdown.value == kong:
                    dropdown.value = ""
        else:
            kong_options = js.document.getElementsByClassName(f"plando-{kong}-option")
            # Re-enable this Kong as a dropdown option.
            for option in kong_options:
                option.removeAttribute("disabled")


startingMoveValues = [str(item.value) for item in StartingMoveOptions]


@bindList("click", startingMoveValues, prefix="none-")
@bindList("click", startingMoveValues, prefix="start-")
@bindList("click", startingMoveValues, prefix="random-")
def plando_disable_starting_moves(evt):
    """Do not allow starting moves to be placed as items."""
    # Create a list of selected starting moves.
    selectedStartingMoves = set()
    for startingMove in startingMoveValues:
        selectedElem = js.document.getElementById(f"start-{startingMove}")
        if selectedElem.checked:
            selectedStartingMoves.add(Items(int(startingMove)))

    # Obtain the list of PlandoItems moves to disable.
    progressiveMoves = [PlandoItems.ProgressiveAmmoBelt, PlandoItems.ProgressiveInstrumentUpgrade, PlandoItems.ProgressiveSlam]
    selectedPlandoMoves = set([ItemToPlandoItemMap[move] for move in selectedStartingMoves if ItemToPlandoItemMap[move] not in progressiveMoves])
    # Progressive moves are handled differently. Only disable these if all
    # instances are included as starting moves.
    if set([Items.ProgressiveSlam, Items.ProgressiveSlam2, Items.ProgressiveSlam3]).issubset(selectedStartingMoves):
        selectedPlandoMoves.add(PlandoItems.ProgressiveSlam)
    if set([Items.ProgressiveAmmoBelt, Items.ProgressiveAmmoBelt2]).issubset(selectedStartingMoves):
        selectedPlandoMoves.add(PlandoItems.ProgressiveAmmoBelt)
    if set([Items.ProgressiveInstrumentUpgrade, Items.ProgressiveInstrumentUpgrade2, Items.ProgressiveInstrumentUpgrade3]).issubset(selectedStartingMoves):
        selectedPlandoMoves.add(PlandoItems.ProgressiveInstrumentUpgrade)

    # Disable all the plando moves across the dropdowns.
    for moveName in MoveSet:
        moveEnum = PlandoItems[moveName]
        # Ignore these moves.
        if moveEnum in {PlandoItems.Camera, PlandoItems.Shockwave}:
            continue
        move_options = js.document.getElementsByClassName(f"plando-{moveName}-option")
        if moveEnum in selectedPlandoMoves:
            # Disable this move as a dropdown option.
            for option in move_options:
                option.setAttribute("disabled", "disabled")
        else:
            # Re-enable this move as a dropdown option.
            for option in move_options:
                option.removeAttribute("disabled")
    # Deselect all the plando moves across the dropdowns.
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    for dropdown in item_dropdowns:
        if dropdown.value == "":
            continue
        move = PlandoItems[dropdown.value]
        if move in selectedPlandoMoves:
            dropdown.value = ""


@bind("change", "dk_colors")
@bind("change", "diddy_colors")
@bind("change", "lanky_colors")
@bind("change", "tiny_colors")
@bind("change", "chunky_colors")
@bind("change", "rambi_colors")
@bind("change", "enguarde_colors")
def hide_rgb(event):
    """Show RGB Selector if Custom Color is selected."""
    for i in ["dk", "diddy", "lanky", "tiny", "chunky", "rambi", "enguarde"]:
        hidden = True
        color = js.document.getElementById(f"{i}_custom")
        if js.document.getElementById(f"{i}_colors").value == "custom":
            hidden = False
        try:
            if hidden or js.document.getElementById("random_colors").checked:
                color.style.display = "none"
            else:
                color.style = ""
        except AttributeError:
            pass


@bind("click", "random_medal_requirement")
def toggle_medals_box(event):
    """Toggle the textbox for Banana Medals."""
    disabled = False
    if js.document.getElementById("random_medal_requirement").checked:
        disabled = True
    medal = js.document.getElementById("medal_requirement")
    if disabled:
        medal.setAttribute("disabled", "disabled")
    else:
        medal.removeAttribute("disabled")


@bind("change", "shockwave_status")
def toggle_extreme_prices_option(event):
    """Determine the visibility of the extreme prices option."""
    unlocked_shockwave = document.getElementById("shockwave_status").value == "start_with"
    logic_disabled = document.getElementById("logic_type").value == "nologic"
    option = document.getElementById("extreme_price_option")
    if unlocked_shockwave or logic_disabled:
        option.removeAttribute("disabled")
    else:
        option.setAttribute("disabled", "disabled")
        price_option = document.getElementById("random_prices")
        if price_option.value == "extreme":
            price_option.value = "high"


@bind("change", "shockwave_status")
def plando_disable_camera_shockwave(evt):
    """Disable placement of camera/shockwave if they are not shuffled."""
    shockwave_status = document.getElementById("shockwave_status").value
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    move_options = js.document.getElementsByClassName(f"plando-camera-shockwave-option")
    disabled = shockwave_status == "start_with" or shockwave_status == "vanilla"
    if disabled:
        # Disable Camera and Shockwave dropdown options.
        for option in move_options:
            option.setAttribute("disabled", "disabled")
        # Remove these items anywhere they've been selected.
        for dropdown in item_dropdowns:
            if dropdown.value == "Camera" or dropdown.value == "Shockwave":
                dropdown.value = ""
    else:
        # Re-enable Camera and Shockwave dropdown options.
        for option in move_options:
            option.removeAttribute("disabled")


@bind("change", "logic_type")
def toggle_logic_type(event):
    """Toggle settings based on the presence of logic."""
    toggle_extreme_prices_option(event)
    glitch_customization = document.getElementById("glitches_modal")
    if document.getElementById("logic_type").value == "glitch":
        glitch_customization.removeAttribute("disabled")
    else:
        glitch_customization.setAttribute("disabled", "disabled")


@bind("change", "bananaport_rando")
def toggle_bananaport_selector(event):
    """Toggle bananaport settings if shuffling is enabled."""
    bananaport_customization = document.getElementById("warp_level_list_modal")
    if document.getElementById("bananaport_rando").value != "off":
        bananaport_customization.removeAttribute("disabled")
    else:
        bananaport_customization.setAttribute("disabled", "disabled")


@bind("click", "nav-patch-tab")
def toggle_patch_ui(event):
    """Disable non-cosmetic tabs if using patch file."""
    for tab in ["nav-started-tab", "nav-random-tab", "nav-overworld-tab", "nav-progression-tab", "nav-qol-tab"]:
        document.getElementById(tab).setAttribute("disabled", "disabled")
    document.getElementById("override_div").removeAttribute("hidden")
    document.getElementById("nav-cosmetics-tab").click()


@bind("click", "nav-seed-gen-tab")
def toggle_patch_ui(event):
    """Re-enable non-cosmetic tabs and hide override option if generating a new seed."""
    for tab in ["nav-started-tab", "nav-random-tab", "nav-overworld-tab", "nav-progression-tab", "nav-qol-tab"]:
        document.getElementById(tab).removeAttribute("disabled")
    document.getElementById("override_div").setAttribute("hidden", "hidden")
    document.getElementById("override_cosmetics").checked = True


@bind("click", "nav-pastgen-tab")
def hide_override_cosmetics(event):
    """Hide the override cosmetics setting when clicking the Generate from Past Seed button."""
    document.getElementById("override_div").setAttribute("hidden", "hidden")
    document.getElementById("override_cosmetics").checked = True


@bind("click", "nav-music-tab")
@bind("change", "music_bgm_randomized")
def rename_default_bgm_options(evt):
    """Rename the default options for BGM music selection."""
    toggleElem = js.document.getElementById(f"music_bgm_randomized")
    defaultOptions = js.document.getElementsByClassName(f"BGM-default-option")
    if toggleElem.checked:
        for opt in defaultOptions:
            opt.innerHTML = "-- Randomize --"
    else:
        for opt in defaultOptions:
            opt.innerHTML = "-- Default --"


@bind("click", "nav-music-tab")
@bind("change", "music_majoritems_randomized")
def rename_default_majoritems_options(evt):
    """Rename the default options for major item music selection."""
    toggleElem = js.document.getElementById(f"music_majoritems_randomized")
    defaultOptions = js.document.getElementsByClassName(f"MajorItem-default-option")
    if toggleElem.checked:
        for opt in defaultOptions:
            opt.innerHTML = "-- Randomize --"
    else:
        for opt in defaultOptions:
            opt.innerHTML = "-- Default --"


@bind("click", "nav-music-tab")
@bind("change", "music_minoritems_randomized")
def rename_default_minoritems_options(evt):
    """Rename the default options for minor item music selection."""
    toggleElem = js.document.getElementById(f"music_minoritems_randomized")
    defaultOptions = js.document.getElementsByClassName(f"MinorItem-default-option")
    if toggleElem.checked:
        for opt in defaultOptions:
            opt.innerHTML = "-- Randomize --"
    else:
        for opt in defaultOptions:
            opt.innerHTML = "-- Default --"


@bind("click", "nav-music-tab")
@bind("change", "music_events_randomized")
def rename_default_events_options(evt):
    """Rename the default options for event music selection."""
    toggleElem = js.document.getElementById(f"music_events_randomized")
    defaultOptions = js.document.getElementsByClassName(f"Event-default-option")
    if toggleElem.checked:
        for opt in defaultOptions:
            opt.innerHTML = "-- Randomize --"
    else:
        for opt in defaultOptions:
            opt.innerHTML = "-- Default --"


@bind("click", "select_keys")
def toggle_key_settings(event):
    """Disable other keys settings when selecting keys. Toggle Key Selector Modal."""
    disabled = False
    if js.document.getElementById("select_keys").checked:
        disabled = True
    krool_access = js.document.getElementById("krool_access")
    keys_random = js.document.getElementById("keys_random")
    selector = js.document.getElementById("starting_keys_list_modal")
    if disabled:
        krool_access.setAttribute("disabled", "disabled")
        krool_access.checked = False
        keys_random.setAttribute("disabled", "disabled")
        selector.removeAttribute("disabled")
    else:
        krool_access.removeAttribute("disabled")
        keys_random.removeAttribute("disabled")
        selector.setAttribute("disabled", "disabled")


@bind("click", "key_8_helm")
@bind("click", "select_keys")
@bind("click", "starting_keys_list_selected")
def plando_disable_keys(evt):
    """Disable keys from being selected for locations in the plandomizer, depending on the current settings."""
    # This dict will map our key strings to enum values.
    keyDict = {1: "JungleJapesKey", 2: "AngryAztecKey", 3: "FranticFactoryKey", 4: "GloomyGalleonKey", 5: "FungiForestKey", 6: "CrystalCavesKey", 7: "CreepyCastleKey", 8: "HideoutHelmKey"}
    # Determine which keys are enabled and which are disabled.
    disabled_keys = set()
    if js.document.getElementById("select_keys").checked:
        starting_keys_list_selected = js.document.getElementById("starting_keys_list_selected")
        # All keys the user starts with are disabled.
        disabled_keys.update({x.value for x in starting_keys_list_selected.selectedOptions})
    # If Key 8 is locked in Helm, it gets disabled.
    if js.document.getElementById("key_8_helm").checked:
        disabled_keys.add("HideoutHelmKey")
    item_dropdowns = js.document.getElementsByClassName("plando-item-select")
    # Look at every key and react if it's enabled or disabled.
    for i in range(1, 9):
        key_string = keyDict[i]
        if key_string in disabled_keys:
            key_options = js.document.getElementsByClassName(f"plando-{key_string}-option")
            # Disable this key as a dropdown option.
            for option in key_options:
                option.setAttribute("disabled", "disabled")
            # De-select this key everywhere it is selected.
            for dropdown in item_dropdowns:
                if dropdown.value == key_string:
                    dropdown.value = ""
        else:
            key_options = js.document.getElementsByClassName(f"plando-{key_string}-option")
            # Re-enable this key as a dropdown option.
            for option in key_options:
                option.removeAttribute("disabled")


@bind("click", "helm_hurry")
def disable_helm_hurry(evt):
    """Disable Helm Hurry Selector when Helm Hurry is off."""
    disabled = True
    selector = js.document.getElementById("helmhurry_list_modal")
    if js.document.getElementById("helm_hurry").checked:
        disabled = False
    try:
        if disabled:
            selector.setAttribute("disabled", "disabled")
        else:
            selector.removeAttribute("disabled")
    except AttributeError:
        pass


@bind("click", "vanilla_door_rando")
def toggle_vanilla_door_rando(evt):
    """Force Wrinkly and T&S Rando to be on when Vanilla Door Rando is on."""
    vanilla_door_shuffle = js.document.getElementById("vanilla_door_rando")
    wrinkly_rando = js.document.getElementById("wrinkly_location_rando")
    tns_rando = js.document.getElementById("tns_location_rando")
    if vanilla_door_shuffle.checked:
        wrinkly_rando.checked = True
        wrinkly_rando.setAttribute("disabled", "disabled")
        tns_rando.checked = True
        tns_rando.setAttribute("disabled", "disabled")
    else:
        wrinkly_rando.removeAttribute("disabled")
        tns_rando.removeAttribute("disabled")


@bind("click", "starting_moves_reset")
def reset_starting_moves(evt):
    """Reset the starting move selector to have nothing selected."""
    for starting_move_button in [element for element in js.document.getElementsByTagName("input") if element.name.startswith("starting_move_box_")]:
        starting_move_button.checked = starting_move_button.id.startswith("none")
    # Update the plandomizer dropdowns.
    plando_disable_starting_moves(evt)


@bind("click", "starting_moves_start_all")
def start_all_starting_moves(evt):
    """Update the starting move selector to start with all items."""
    for starting_move_button in [element for element in js.document.getElementsByTagName("input") if element.name.startswith("starting_move_box_")]:
        starting_move_button.checked = starting_move_button.id.startswith("start")
    # Update the plandomizer dropdowns.
    plando_disable_starting_moves(evt)


@bind("click", "randomize_settings")
def shuffle_settings(evt):
    """Randomize all non-cosmetic settings."""
    randomize_settings()

    # Run additional functions to ensure there are no conflicts.
    updateDoorOneNumAccess(None)
    updateDoorOneCountText(None)
    updateDoorTwoNumAccess(None)
    updateDoorTwoCountText(None)
    toggle_b_locker_boxes(None)
    toggle_counts_boxes(None)
    update_boss_required(None)
    disable_tag_spawn(None)
    disable_krool_phases(None)
    disable_helm_phases(None)
    disable_move_shuffles(None)
    disable_barrel_modal(None)
    disable_enemy_modal(None)
    disable_hard_mode_modal(None)
    item_rando_list_changed(None)
    enable_plandomizer(None)
    disable_switchsanity_with_plandomizer(None)
    toggle_medals_box(None)
    toggle_extreme_prices_option(None)
    toggle_logic_type(None)
    toggle_bananaport_selector(None)
    toggle_key_settings(None)
    disable_helm_hurry(None)
    toggle_vanilla_door_rando(None)


musicToggles = [category.replace(" ", "") for category in MusicSelectionPanel.keys()]


@bind("click", "settings_table_collapse_toggle")
@bindList("click", musicToggles, suffix="_collapse_toggle")
def toggle_settings_table(evt):
    targetElement = evt.target
    if "collapse_toggle" not in targetElement.id:
        # Get the parent of this element.
        targetElement = targetElement.parentElement
    toggledElement = re.search("^(.+)_collapse_toggle$", targetElement.id)[1]
    """Open or close the settings table on the Seed Info tab."""
    settingsTable = js.document.getElementById(toggledElement)
    settingsTable.classList.toggle("collapsed")
    toggledArrow = f'{toggledElement.replace("_", "-")}-expand-arrow'
    settingsArrow = js.document.getElementsByClassName(toggledArrow).item(0)
    settingsArrow.classList.toggle("flipped")
