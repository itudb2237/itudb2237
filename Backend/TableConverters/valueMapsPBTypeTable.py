
HeadMappings = {
"ST_CASE": "CASE_NUMBER",
"VEH_NO":  "VEHICLE_NUMBER",
"PER_NO": "PERSON_NUMBER",
"PBPTYPE": "PERSON_TYPE",
"PBCWALK":"CROSSWALK_PRESENT",
"PBSWALK": "SIDEWALK_PRESENT",
"PBSZONE": "SCHOOLZONE_PRESENT",
"MOTMAN": "MOTOR_MANEUVER"}

ValueMappings = {"PERSON_TYPE": {
                     5: "Pedestrian",
                     6: "Bicyclist",
                     7: "Other Cyclist",
                     8: "Person on Personal Conveyances",
                },
                 "CROSSWALK_PRESENT": {
                    0: "None Noted",
                    1: "Yes",
                    9: "Unknown"
                 },
                 "SIDEWALK_PRESENT": {
                    0: "None Noted",
                    1: "Yes",
                    9: "Unknown"
                 },
                 "SCHOOLZONE_PRESENT": {
                    0: "None Noted",
                    1: "Yes",
                    9: "Unknown"
                 },
                 "MOTOR_MANEUVER": {
                    1: "Left Turn",
                    2: "Right Turn",
                    3: "Straight Through",
                    7: "Not a Pedestrian",
                    8: "Not Applicable",
                    9: "Unknown Motorist Maneuver"
                 }
                 }
