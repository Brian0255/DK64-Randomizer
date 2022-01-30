#include "../../include/common.h"

#define GLOOMY_GALLEON 0x1E
#define ANGRY_AZTEC 0x26
#define CRYSTAL_CAVES 0x48

void load_object_script(int obj_instance_id) {
	scriptLoadsAttempted += 1;
	int script_index = scriptsLoaded;
	if (script_index != 0x46) {
		scriptsLoaded = script_index + 1;
		scriptLoadedArray[script_index] = obj_instance_id;
		int obj_idx = convertIDToIndex(obj_instance_id);
		int* m2location = ObjectModel2Pointer;
		ModelTwoData* _object = getObjectArrayAddr(m2location,0x90,obj_idx);
		int* behav = _object->behaviour_pointer;
		updateObjectScript(behav);
		executeBehaviourScript(behav, obj_instance_id);
	}
}

void adjust_galleon_water(void) {
	if (ObjectModel2Timer < 5) {
		if (CurrentMap == GLOOMY_GALLEON) {
			load_object_script(0);
			if (checkFlag(160,0)) {
				for (int i = 0; i < 20; i++) {
					setWaterHeight(i,55.0f,1000.0f);
				}
			}
		} else if (CurrentMap == ANGRY_AZTEC) {
			load_object_script(0xC1);
		} else if (CurrentMap == CRYSTAL_CAVES) {
			load_object_script(0x31);
		}
	}
}