class_names = ['aeroplane', 'bicycle', 'bird', 'boat', 'bottle',
                   'bus', 'car', 'cat', 'chair', 'cow',
                   'diningtable', 'dog', 'horse', 'motorbike', 'person',
                   'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor',
                   ]
                   
new_class_names = ['aeroplane', 'bicycle', 'bird avian', 'boat', 'bottle',
                   'bus', 'car', 'cat', 'chair seat', 'cow',
                   'diningtable', 'dog', 'horse', 'motorbike', 'person with clothes,people,human',
                   'pottedplant', 'sheep', 'sofa', 'train', 'tvmonitor screen',
                   ]

class_text_descriptions = {
    "aeroplane": [
        "A clean origami aeroplane. It has a streamlined fuselage, large wings with a fixed span, and a prominent tail fin.",
        "A clean origami aeroplane. It features a pointed nose, retractable landing gear, and windows along the cabin side.",
        "A clean origami aeroplane. It is characterized by swept-back wings, multiple engines mounted under the wings.",
        "A clean origami aeroplane. It displays a tapered body shape, vertical stabilizers, and an elevated cockpit section.",
        "A clean origami aeroplane. It shows smooth aerodynamic surfaces and winglets at the wingtips."
    ],
    "bicycle": [
        "A clean origami bicycle. It features two circular wheels connected by a frame, a saddle seat, and handlebars for steering.",
        "A clean origami bicycle. It has a triangular or diamond-shaped frame, pedals attached to cranks, and a chain linking to the rear wheel.",
        "A clean origami bicycle. It displays thin rubber tires, a front fork for suspension, and often includes a rack or basket.",
        "A clean origami bicycle. It is characterized by a lightweight metal frame, hand brakes on the handlebars, and reflectors on the wheels.",
        "A clean origami bicycle. It shows a simple mechanical structure, a gear system for speed adjustment, and often painted in bright colors."
    ],
    "bird avian": [
        "A clean origami bird avian. It has a small body covered with feathers, a pointed beak, and two wings for flying.",
        "A clean origami bird avian. It features a rounded head, two legs with claws, and a tail that helps with balance.",
        "A clean origami bird avian. It displays vibrant plumage often in colors like blue, red, or yellow, and a lightweight skeletal structure.",
        "A clean origami bird avian. It is characterized by a curved beak suitable for eating seeds or insects, and eyes positioned on the sides.",
        "A clean origami bird avian. It shows a streamlined body shape, a breastbone with a keel for wing muscle attachment."
    ],
    "boat": [
        "A clean origami boat. It has a curved hull that floats on water, a pointed bow, and a flat stern.",
        "A clean origami boat. It features a mast or sail for wind propulsion, a cabin for shelter, and often painted in white or blue.",
        "A clean origami boat. It displays a long narrow shape, oarlocks for rowing, and a rudder at the back for steering.",
        "A clean origami boat. It is characterized by a deck surface, windows or portholes along the sides, and sometimes an outboard motor.",
        "A clean origami boat. It shows a waterproof exterior made of wood or fiberglass and a railing around the edges."
    ],
    "bottle": [
        "A clean origami bottle. It has a cylindrical or curved body, a narrow neck, and a cap or cork for sealing.",
        "A clean origami bottle. It features a smooth glass or plastic surface, a label area on the front, and a flat base for stability.",
        "A clean origami bottle. It displays a transparent or colored material, a screw-top or flip-top lid, and often contains liquid.",
        "A clean origami bottle. It is characterized by a rounded shoulder near the neck and a cylindrical shape.",
        "A clean origami bottle. It shows a slender profile and a mouth opening for pouring."
    ],
    "bus": [
        "A clean origami bus. It has a large rectangular body, multiple large windows along the sides, and a flat front with a windshield.",
        "A clean origami bus. It features a long chassis, multiple wheels, and often painted in bright colors like yellow or red.",
        "A clean origami bus. It displays a high roofline, doors for entry and exit, and a rear engine compartment.",
        "A clean origami bus. It is characterized by a boxy shape, a front grille and headlights, and often includes advertising.",
        "A clean origami bus. It shows a spacious interior visible through windows and a side mirror on each side."
    ],
    "car": [
        "A clean origami car. It has a compact body with four wheels, a front grille, and headlights on either side.",
        "A clean origami car. It features a windshield, side windows, and doors for entry, often painted in metallic colors.",
        "A clean origami car. It displays a curved roof, a rear trunk, and a license plate on the back.",
        "A clean origami car. It is characterized by a hood covering the engine, a dashboard inside, and side mirrors.",
        "A clean origami car. It shows a streamlined shape and wheel arches."
    ],
    "cat": [
        "A clean origami cat. It has a small furry body, pointy ears, and a long tail that often curls.",
        "A clean origami cat. It features whiskers on the muzzle, slit-shaped pupils, and padded paws with retractable claws.",
        "A clean origami cat. It displays a graceful posture, a triangular nose, and fur patterns such as stripes or spots.",
        "A clean origami cat. It is characterized by a flexible spine, a short muzzle, and often seen in colors like gray or orange.",
        "A clean origami cat. It shows a slender build and almond-shaped eyes."
    ],
    "chair seat": [
        "A clean origami chair seat. It has a flat horizontal seat surface, a vertical backrest, and four legs for support.",
        "A clean origami chair seat. It features a simple rectangular or curved design, often made of wood or plastic.",
        "A clean origami chair seat. It displays armrests on the sides, a cushioned seat, and sometimes wheels on the legs.",
        "A clean origami chair seat. It is characterized by a sturdy frame and a slatted or upholstered back.",
        "A clean origami chair seat. It shows a functional structure and a seat height suitable for sitting at a table."
    ],
    "cow": [
        "A clean origami cow. It has a large body with four legs, a broad muzzle, and two curved horns on the head.",
        "A clean origami cow. It features a black-and-white or brown spotted coat and a long tail with a tufted end.",
        "A clean origami cow. It displays a heavy build, a dewlap under the neck, and a calm grazing posture.",
        "A clean origami cow. It is characterized by a rectangular body shape, cloven hooves, and ears that point sideways.",
        "A clean origami cow. It shows a gentle expression and a wide nose."
    ],
    "diningtable": [
        "A clean origami diningtable. It has a flat rectangular or round top surface supported by four legs.",
        "A clean origami diningtable. It features a smooth tabletop often made of wood or glass and a central pedestal.",
        "A clean origami diningtable. It displays a sturdy construction and a surface for placing plates and utensils.",
        "A clean origami diningtable. It is characterized by a polished finish and a uniform height suitable for chairs.",
        "A clean origami diningtable. It shows a simple geometric design and edges that may be rounded or straight."
    ],
    "dog": [
        "A clean origami dog. It has a furry body, floppy or pointed ears, and a tail that wags.",
        "A clean origami dog. It features a moist nose, four legs with paws, and often wears a collar.",
        "A clean origami dog. It displays a variety of coat textures and colors such as brown, black, or white.",
        "A clean origami dog. It is characterized by a loyal expression and a muzzle of medium length.",
        "A clean origami dog. It shows a compact or slender build and a tongue that may hang out."
    ],
    "horse": [
        "A clean origami horse. It has a tall body with long legs, a flowing mane, and a tail that reaches the ground.",
        "A clean origami horse. It features a strong muscular build, a long neck, and hooves often shod with horseshoes.",
        "A clean origami horse. It displays a smooth coat in colors like brown, black, or white and a distinctive saddle area.",
        "A clean origami horse. It is characterized by a graceful galloping posture and large expressive eyes.",
        "A clean origami horse. It shows a powerful chest and a narrow waist."
    ],
    "motorbike": [
        "A clean origami motorbike. It has two wheels aligned in a line, a seat for the rider, and handlebars for steering.",
        "A clean origami motorbike. It features an engine mounted between the wheels, a fuel tank above, and an exhaust pipe.",
        "A clean origami motorbike. It displays a sleek metallic frame, a headlight at the front, and footpegs for the rider.",
        "A clean origami motorbike. It is characterized by a compact design and a rear suspension system.",
        "A clean origami motorbike. It shows a minimal body covering and a chain or belt drive to the rear wheel."
    ],
    "person with clothes,people,human": [
        "A clean origami person with clothes,people,human. It has a head on top, a torso in the middle, and two arms and two legs.",
        "A clean origami person with clothes,people,human. It features clothing such as a shirt and pants and an upright posture.",
        "A clean origami person with clothes,people,human. It displays facial features like eyes, nose, and mouth and hair on the head.",
        "A clean origami person with clothes,people,human. It is characterized by a bipedal stance and hands with fingers.",
        "A clean origami person with clothes,people,human. It shows a variety of poses such as walking, sitting, or gesturing."
    ],
    "pottedplant": [
        "A clean origami pottedplant. It has a container or pot holding soil with green leaves or stems growing upward.",
        "A clean origami pottedplant. It features a central stem or multiple branches and leaves that may be broad or narrow.",
        "A clean origami pottedplant. It displays a simple decorative pot often in terracotta or ceramic.",
        "A clean origami pottedplant. It is characterized by a compact growth habit and a root system hidden inside the pot.",
        "A clean origami pottedplant. It shows a natural green color and a pot with a drainage hole."
    ],
    "sheep": [
        "A clean origami sheep. It has a fluffy woolly coat covering most of its body, a short tail, and a blunt muzzle.",
        "A clean origami sheep. It features curled horns on some breeds, cloven hooves, and a gentle grazing posture.",
        "A clean origami sheep. It displays a rounded body shape and a face often left uncovered by wool.",
        "A clean origami sheep. It is characterized by a thick fleece that may be white, black, or brown.",
        "A clean origami sheep. It shows a compact build and a tendency to flock together."
    ],
    "sofa": [
        "A clean origami sofa. It has a long cushioned seat for multiple people, a backrest, and armrests on both ends.",
        "A clean origami sofa. It features an upholstered surface in fabric or leather and often includes throw pillows.",
        "A clean origami sofa. It displays a sturdy wooden or metal frame underneath and a padded seat.",
        "A clean origami sofa. It is characterized by a rectangular shape and a seat height lower than a chair.",
        "A clean origami sofa. It shows a cohesive design and seams or buttons on the surface."
    ],
    "train": [
        "A clean origami train. It has a series of connected cars on rails, a locomotive at the front, and windows along the sides.",
        "A clean origami train. It features a long rectangular shape and wheels hidden under the body.",
        "A clean origami train. It displays a smokestack or pantograph on the roof and coupling mechanisms between cars.",
        "A clean origami train. It is characterized by a metallic body and a consistent height above the tracks.",
        "A clean origami train. It shows a streamlined front section and a uniform row of windows."
    ],
    "tvmonitor screen": [
        "A clean origami tvmonitor screen. It has a flat rectangular screen, a bezel around the edges, and a stand or wall mount.",
        "A clean origami tvmonitor screen. It features a black or dark frame and a smooth glass surface.",
        "A clean origami tvmonitor screen. It displays a thin profile and control buttons or ports on the side.",
        "A clean origami tvmonitor screen. It is characterized by a widescreen aspect ratio and a glossy or matte finish.",
        "A clean origami tvmonitor screen. It shows a simple geometric shape and a screen that may be on or off."
    ]
}

class_names_coco = ['person','bicycle','car','motorbike','aeroplane',
                    'bus','train','truck','boat','traffic light',
                    'fire hydrant','stop sign','parking meter','bench','bird',
                    'cat','dog','horse','sheep','cow',
                    'elephant','bear','zebra','giraffe','backpack',
                    'umbrella','handbag','tie','suitcase','frisbee',
                    'skis','snowboard','sports ball','kite','baseball bat',
                    'baseball glove','skateboard','surfboard','tennis racket','bottle',
                    'wine glass','cup','fork','knife','spoon',
                    'bowl','banana','apple','sandwich','orange',
                    'broccoli','carrot','hot dog','pizza','donut',
                    'cake','chair','sofa','pottedplant','bed',
                    'diningtable','toilet','tvmonitor','laptop','mouse',
                    'remote','keyboard','cell phone','microwave','oven',
                    'toaster','sink','refrigerator','book','clock',
                    'vase','scissors','teddy bear','hair drier','toothbrush',
]

new_class_names_coco = ['person with clothes,people,human','bicycle','car','motorbike','aeroplane',
                    'bus','train','truck','boat','traffic light',
                    'fire hydrant','stop sign','parking meter','bench','bird avian',
                    'cat','dog','horse','sheep','cow',
                    'elephant','bear','zebra','giraffe','backpack,bag',
                    'umbrella,parasol','handbag,purse','necktie','suitcase','frisbee',
                    'skis','sknowboard','sports ball','kite','baseball bat',
                    'glove','skateboard','surfboard','tennis racket','bottle',
                    'wine glass','cup','fork','knife','dessertspoon',
                    'bowl','banana','apple','sandwich','orange',
                    'broccoli','carrot','hot dog','pizza','donut',
                    'cake','chair seat','sofa','pottedplant','bed',
                    'diningtable','toilet','tvmonitor screen','laptop','mouse',
                    'remote control','keyboard','cell phone','microwave','oven',
                    'toaster','sink','refrigerator','book','clock',
                    'vase','scissors','teddy bear','hairdrier,blowdrier','toothbrush',
                    ]


new_class_names_coco2 = ['person with clothes,people,human','bicycle','car','motorbike','aeroplane',
                    'bus','train','truck','boat','traffic light',
                    'fire hydrant','stop sign','parking meter','bench','bird avian',
                    'cat','dog','horse','sheep','cow',
                    'elephant','bear','zebra','giraffe','backpack,bag',
                    'umbrella,parasol','handbag,purse','necktie','suitcase','frisbee',
                    'skis','sknowboard','sports ball','kite','baseball bat',
                    'glove','skateboard','surfboard','tennis racket','bottle',
                    'wine glass','cup','fork','knife','dessertspoon',
                    'bowl','banana','apple','sandwich','orange',
                    'broccoli','carrot','hot dog','pizza','donut',
                    'cake','chair seat','sofa','pottedplant','bed',
                    'diningtable','toilet','tvmonitor screen','laptop','mouse',
                    'remote control','keyboard','cell phone','microwave','oven',
                    'toaster','sink','refrigerator','book','clock',
                    'vase','scissors','teddy bear','hairdrier,blowdrier','toothbrush',
                    ]

class_text_descriptions_coco = {
    "person with clothes,people,human": [
        "A clean origami person with clothes,people,human. It has a head on top, a torso in the middle, and two arms and two legs.",
        "A clean origami person with clothes,people,human. It features clothing such as a shirt and pants and an upright posture.",
        "A clean origami person with clothes,people,human. It displays facial features like eyes, nose, and mouth and hair on the head.",
        "A clean origami person with clothes,people,human. It is characterized by a bipedal stance and hands with fingers.",
        "A clean origami person with clothes,people,human. It shows a variety of poses such as walking, sitting, or gesturing."
    ],
    "bicycle": [
        "A clean origami bicycle. It features two circular wheels connected by a frame, a saddle seat, and handlebars for steering.",
        "A clean origami bicycle. It has a triangular or diamond-shaped frame, pedals attached to cranks, and a chain linking to the rear wheel.",
        "A clean origami bicycle. It displays thin rubber tires, a front fork for suspension, and often includes a rack or basket.",
        "A clean origami bicycle. It is characterized by a lightweight metal frame, hand brakes on the handlebars, and reflectors on the wheels.",
        "A clean origami bicycle. It shows a simple mechanical structure, a gear system for speed adjustment, and often painted in bright colors."
    ],
    "car": [
        "A clean origami car. It has a compact body with four wheels, a front grille, and headlights on either side.",
        "A clean origami car. It features a windshield, side windows, and doors for entry, often painted in metallic colors.",
        "A clean origami car. It displays a curved roof, a rear trunk, and a license plate on the back.",
        "A clean origami car. It is characterized by a hood covering the engine, a dashboard inside, and side mirrors.",
        "A clean origami car. It shows a streamlined shape and wheel arches."
    ],
    "motorbike": [
        "A clean origami motorbike. It has two wheels aligned in a line, a seat for the rider, and handlebars for steering.",
        "A clean origami motorbike. It features an engine mounted between the wheels, a fuel tank above, and an exhaust pipe.",
        "A clean origami motorbike. It displays a sleek metallic frame, a headlight at the front, and footpegs for the rider.",
        "A clean origami motorbike. It is characterized by a compact design and a rear suspension system.",
        "A clean origami motorbike. It shows a minimal body covering and a chain or belt drive to the rear wheel."
    ],
    "aeroplane": [
        "A clean origami aeroplane. It has a streamlined fuselage, large wings with a fixed span, and a prominent tail fin.",
        "A clean origami aeroplane. It features a pointed nose, retractable landing gear, and windows along the cabin side.",
        "A clean origami aeroplane. It is characterized by swept-back wings, multiple engines mounted under the wings.",
        "A clean origami aeroplane. It displays a tapered body shape, vertical stabilizers, and an elevated cockpit section.",
        "A clean origami aeroplane. It shows smooth aerodynamic surfaces and winglets at the wingtips."
    ],
    "bus": [
        "A clean origami bus. It has a large rectangular body, multiple large windows along the sides, and a flat front with a windshield.",
        "A clean origami bus. It features a long chassis, multiple wheels, and often painted in bright colors like yellow or red.",
        "A clean origami bus. It displays a high roofline, doors for entry and exit, and a rear engine compartment.",
        "A clean origami bus. It is characterized by a boxy shape, a front grille and headlights, and often includes advertising.",
        "A clean origami bus. It shows a spacious interior visible through windows and a side mirror on each side."
    ],
    "train": [
        "A clean origami train. It has a series of connected cars on rails, a locomotive at the front, and windows along the sides.",
        "A clean origami train. It features a long rectangular shape and wheels hidden under the body.",
        "A clean origami train. It displays a smokestack or pantograph on the roof and coupling mechanisms between cars.",
        "A clean origami train. It is characterized by a metallic body and a consistent height above the tracks.",
        "A clean origami train. It shows a streamlined front section and a uniform row of windows."
    ],
    "truck": [
        "A clean origami truck. It has a large rectangular cargo area at the back, a cab for the driver, and multiple heavy-duty wheels.",
        "A clean origami truck. It features a long chassis, a front grille and headlights, and often painted in solid colors.",
        "A clean origami truck. It displays a high ground clearance, side mirrors, and sometimes a trailer hitch.",
        "A clean origami truck. It is characterized by a powerful engine compartment and a spacious cab with windows.",
        "A clean origami truck. It shows a utilitarian design and often carries goods or containers."
    ],
    "boat": [
        "A clean origami boat. It has a curved hull that floats on water, a pointed bow, and a flat stern.",
        "A clean origami boat. It features a mast or sail for wind propulsion, a cabin for shelter, and often painted in white or blue.",
        "A clean origami boat. It displays a long narrow shape, oarlocks for rowing, and a rudder at the back for steering.",
        "A clean origami boat. It is characterized by a deck surface, windows or portholes along the sides, and sometimes an outboard motor.",
        "A clean origami boat. It shows a waterproof exterior made of wood or fiberglass and a railing around the edges."
    ],
    "traffic light": [
        "A clean origami traffic light. It has a vertical pole with multiple colored lights arranged in a vertical or horizontal row.",
        "A clean origami traffic light. It features red, yellow, and green circular lights, and a black or gray housing.",
        "A clean origami traffic light. It displays a simple geometric shape, often mounted at intersections, and visible from a distance.",
        "A clean origami traffic light. It is characterized by a standard color sequence and a sturdy metal or plastic construction.",
        "A clean origami traffic light. It shows a functional design and is often attached to a pole or overhead structure."
    ],
    "fire hydrant": [
        "A clean origami fire hydrant. It has a short cylindrical shape, multiple connection ports, and a bright red or yellow color.",
        "A clean origami fire hydrant. It features a valve mechanism on top, a sturdy metal construction, and a bolted base.",
        "A clean origami fire hydrant. It displays a compact design, often found on sidewalks, and painted in highly visible colors.",
        "A clean origami fire hydrant. It is characterized by a recognizable shape with protruding nozzles and a cap for water access.",
        "A clean origami fire hydrant. It shows a utilitarian appearance and is essential for firefighting purposes."
    ],
    "stop sign": [
        "A clean origami stop sign. It has an octagonal shape, a bright red background, and the word 'STOP' in white letters.",
        "A clean origami stop sign. It features a reflective surface for visibility at night, and a metal pole for support.",
        "A clean origami stop sign. It displays a simple geometric design, standardized proportions, and bold typography.",
        "A clean origami stop sign. It is characterized by its unique eight-sided shape and high-contrast color scheme.",
        "A clean origami stop sign. It shows a functional traffic control device often placed at intersections."
    ],
    "parking meter": [
        "A clean origami parking meter. It has a tall narrow body with a coin slot, a display screen, and a timer mechanism.",
        "A clean origami parking meter. It features a simple metal or plastic housing, often painted in gray or silver.",
        "A clean origami parking meter. It displays a digital or analog display, a payment slot, and a pole for mounting.",
        "A clean origami parking meter. It is characterized by a utilitarian design and is typically found along curbsides.",
        "A clean origami parking meter. It shows a compact structure and is used for collecting parking fees."
    ],
    "bench": [
        "A clean origami bench. It has a long flat seat supported by legs or a solid base, often made of wood or metal.",
        "A clean origami bench. It features a simple design, a backrest in some models, and space for multiple people.",
        "A clean origami bench. It displays a sturdy construction, often found in parks or public spaces, and painted in neutral colors.",
        "A clean origami bench. It is characterized by a functional shape and a surface suitable for sitting.",
        "A clean origami bench. It shows a rectangular or curved profile and is designed for outdoor or indoor use."
    ],
    "bird avian": [
        "A clean origami bird avian. It has a small body covered with feathers, a pointed beak, and two wings for flying.",
        "A clean origami bird avian. It features a rounded head, two legs with claws, and a tail that helps with balance.",
        "A clean origami bird avian. It displays vibrant plumage often in colors like blue, red, or yellow, and a lightweight skeletal structure.",
        "A clean origami bird avian. It is characterized by a curved beak suitable for eating seeds or insects, and eyes positioned on the sides.",
        "A clean origami bird avian. It shows a streamlined body shape, a breastbone with a keel for wing muscle attachment."
    ],
    "cat": [
        "A clean origami cat. It has a small furry body, pointy ears, and a long tail that often curls.",
        "A clean origami cat. It features whiskers on the muzzle, slit-shaped pupils, and padded paws with retractable claws.",
        "A clean origami cat. It displays a graceful posture, a triangular nose, and fur patterns such as stripes or spots.",
        "A clean origami cat. It is characterized by a flexible spine, a short muzzle, and often seen in colors like gray or orange.",
        "A clean origami cat. It shows a slender build and almond-shaped eyes."
    ],
    "dog": [
        "A clean origami dog. It has a furry body, floppy or pointed ears, and a tail that wags.",
        "A clean origami dog. It features a moist nose, four legs with paws, and often wears a collar.",
        "A clean origami dog. It displays a variety of coat textures and colors such as brown, black, or white.",
        "A clean origami dog. It is characterized by a loyal expression and a muzzle of medium length.",
        "A clean origami dog. It shows a compact or slender build and a tongue that may hang out."
    ],
    "horse": [
        "A clean origami horse. It has a tall body with long legs, a flowing mane, and a tail that reaches the ground.",
        "A clean origami horse. It features a strong muscular build, a long neck, and hooves often shod with horseshoes.",
        "A clean origami horse. It displays a smooth coat in colors like brown, black, or white and a distinctive saddle area.",
        "A clean origami horse. It is characterized by a graceful galloping posture and large expressive eyes.",
        "A clean origami horse. It shows a powerful chest and a narrow waist."
    ],
    "sheep": [
        "A clean origami sheep. It has a fluffy woolly coat covering most of its body, a short tail, and a blunt muzzle.",
        "A clean origami sheep. It features curled horns on some breeds, cloven hooves, and a gentle grazing posture.",
        "A clean origami sheep. It displays a rounded body shape and a face often left uncovered by wool.",
        "A clean origami sheep. It is characterized by a thick fleece that may be white, black, or brown.",
        "A clean origami sheep. It shows a compact build and a tendency to flock together."
    ],
    "cow": [
        "A clean origami cow. It has a large body with four legs, a broad muzzle, and two curved horns on the head.",
        "A clean origami cow. It features a black-and-white or brown spotted coat and a long tail with a tufted end.",
        "A clean origami cow. It displays a heavy build, a dewlap under the neck, and a calm grazing posture.",
        "A clean origami cow. It is characterized by a rectangular body shape, cloven hooves, and ears that point sideways.",
        "A clean origami cow. It shows a gentle expression and a wide nose."
    ],
    "elephant": [
        "A clean origami elephant. It has a massive gray body, a long trunk, and large flapping ears.",
        "A clean origami elephant. It features tusks made of ivory, thick legs, and a tail with a tuft of hair at the end.",
        "A clean origami elephant. It displays a wrinkled skin texture, a domed head, and a curved back.",
        "A clean origami elephant. It is characterized by its large size, a trunk used for grasping, and a herbivorous diet.",
        "A clean origami elephant. It shows a distinctive silhouette with a trunk and tusks."
    ],
    "bear": [
        "A clean origami bear. It has a large furry body, rounded ears, and a short tail.",
        "A clean origami bear. It features a massive head, strong limbs with claws, and a hump on its shoulders.",
        "A clean origami bear. It displays a thick coat in colors like brown, black, or white, and a plantigrade walk.",
        "A clean origami bear. It is characterized by a powerful build, a keen sense of smell, and a omnivorous diet.",
        "A clean origami bear. It shows a robust physique and a lumbering gait."
    ],
    "zebra": [
        "A clean origami zebra. It has a horse-like body covered with black and white stripes, a mane, and a tail.",
        "A clean origami zebra. It features a slender build, long legs, and hooves for running.",
        "A clean origami zebra. It displays a unique striping pattern that varies between individuals and a herbivorous diet.",
        "A clean origami zebra. It is characterized by a social behavior, living in herds, and a preference for grasslands.",
        "A clean origami zebra. It shows a graceful running posture and alert ears."
    ],
    "giraffe": [
        "A clean origami giraffe. It has an extremely long neck, long legs, and a coat with irregular brown patches.",
        "A clean origami giraffe. It features ossicones on its head, a prehensile tongue, and a tall stature.",
        "A clean origami giraffe. It displays a spotted pattern, a sloping back, and a tail with a tuft.",
        "A clean origami giraffe. It is characterized by being the tallest land animal and a herbivorous browser.",
        "A clean origami giraffe. It shows a distinctive silhouette with a long neck and legs."
    ],
    "backpack,bag": [
        "A clean origami backpack,bag. It has a main compartment for carrying items, shoulder straps, and often a zipper closure.",
        "A clean origami backpack,bag. It features multiple pockets, a padded back for comfort, and a rectangular shape.",
        "A clean origami backpack,bag. It displays a durable fabric construction, a handle on top, and often reflective details.",
        "A clean origami backpack,bag. It is characterized by a portable design and is worn on the back.",
        "A clean origami backpack,bag. It shows a functional accessory for students or travelers."
    ],
    "umbrella,parasol": [
        "A clean origami umbrella,parasol. It has a circular canopy that opens to provide shelter from rain or sun.",
        "A clean origami umbrella,parasol. It features a central pole, a handle for gripping, and a collapsible design.",
        "A clean origami umbrella,parasol. It displays a curved canopy, often made of waterproof fabric, and a mechanical opening mechanism.",
        "A clean origami umbrella,parasol. It is characterized by a portable and foldable structure for easy carrying.",
        "A clean origami umbrella,parasol. It shows a simple yet effective design for weather protection."
    ],
    "handbag,purse": [
        "A clean origami handbag,purse. It has a small bag with a handle or strap, often used by women to carry personal items.",
        "A clean origami handbag,purse. It features a clasp or zipper closure, an interior compartment, and sometimes a brand logo.",
        "A clean origami handbag,purse. It displays a variety of shapes (e.g., tote, clutch) and materials like leather or fabric.",
        "A clean origami handbag,purse. It is characterized by a fashionable accessory that complements clothing.",
        "A clean origami handbag,purse. It shows a compact design and is often carried in the hand or over the shoulder."
    ],
    "necktie": [
        "A clean origami necktie. It has a long strip of fabric that is worn around the neck and tied in a knot.",
        "A clean origami necktie. It features a tapered shape, a wider end, and often a pattern or solid color.",
        "A clean origami necktie. It displays a smooth texture, a lining inside, and a loop for the thin end.",
        "A clean origami necktie. It is characterized by a formal accessory worn with dress shirts and suits.",
        "A clean origami necktie. It shows a simple yet elegant design for professional or formal occasions."
    ],
    "suitcase": [
        "A clean origami suitcase. It has a rectangular hard or soft case with a handle and wheels for travel.",
        "A clean origami suitcase. It features a zipper closure, a telescopic handle, and a lock for security.",
        "A clean origami suitcase. It displays a durable exterior, a spacious interior, and often a brand tag.",
        "A clean origami suitcase. It is characterized by a portable luggage item for transporting clothes and belongings.",
        "A clean origami suitcase. It shows a practical design for travelers and comes in various sizes."
    ],
    "frisbee": [
        "A clean origami frisbee. It has a flat disc shape that is thrown through the air for recreational play.",
        "A clean origami frisbee. It features a curved rim, a smooth surface, and often bright colors or designs.",
        "A clean origami frisbee. It displays a lightweight plastic construction and an aerodynamic profile.",
        "A clean origami frisbee. It is characterized by a flying toy used in outdoor games and sports.",
        "A clean origami frisbee. It shows a simple circular design that glides when thrown."
    ],
    "skis": [
        "A clean origami skis. It has a pair of long, narrow boards with upturned tips, used for gliding over snow.",
        "A clean origami skis. It features bindings to attach boots, a curved shape for turning, and a smooth bottom surface.",
        "A clean origami skis. It displays a lightweight yet sturdy construction, often made of composite materials.",
        "A clean origami skis. It is characterized by a winter sports equipment for skiing down slopes.",
        "A clean origami skis. It shows a streamlined design for speed and maneuverability on snow."
    ],
    "sknowboard": [
        "A clean origami sknowboard. It has a single wide board with bindings for both feet, used for snowboarding.",
        "A clean origami sknowboard. It features a curved tip and tail, a smooth base, and metal edges for control.",
        "A clean origami sknowboard. It displays a graphic design on the top surface and a length suited to the rider.",
        "A clean origami sknowboard. It is characterized by a winter sports equipment for descending snow-covered slopes.",
        "A clean origami sknowboard. It shows a symmetrical or directional shape for freestyle or alpine riding."
    ],
    "sports ball": [
        "A clean origami sports ball. It has a spherical shape used in various sports like soccer, basketball, or volleyball.",
        "A clean origami sports ball. It features a textured surface for grip, an inflated interior, and often a pattern of panels.",
        "A clean origami sports ball. It displays a standard size and weight according to the sport, and a durable outer cover.",
        "A clean origami sports ball. It is characterized by a universal toy and sports equipment for games and exercise.",
        "A clean origami sports ball. It shows a round shape that bounces and rolls."
    ],
    "kite": [
        "A clean origami kite. It has a lightweight frame covered with paper or fabric, flown in the wind with a string.",
        "A clean origami kite. It features a tail for stability, a bridle to attach the string, and often a colorful design.",
        "A clean origami kite. It displays a diamond, delta, or box shape, and a structure that catches the wind.",
        "A clean origami kite. It is characterized by a recreational outdoor toy that soars in the sky.",
        "A clean origami kite. It shows a simple yet elegant design for flying on windy days."
    ],
    "baseball bat": [
        "A clean origami baseball bat. It has a long, rounded wooden or metal club used to hit a baseball.",
        "A clean origami baseball bat. It features a handle at one end, a barrel at the other, and a tapered shape.",
        "A clean origami baseball bat. It displays a smooth surface, a knob at the handle end, and often a brand logo.",
        "A clean origami baseball bat. It is characterized by a sports equipment used in the game of baseball.",
        "A clean origami baseball bat. It shows a cylindrical shape and is swung to strike the ball."
    ],
    "glove": [
        "A clean origami glove. It has a covering for the hand with separate sections for each finger and the thumb.",
        "A clean origami glove. It features a palm, a back, and a closure at the wrist, made of fabric or leather.",
        "A clean origami glove. It displays a form-fitting design, often used for warmth, protection, or sports.",
        "A clean origami glove. It is characterized by a hand accessory that provides grip or insulation.",
        "A clean origami glove. It shows a five-fingered pattern and is worn on one or both hands."
    ],
    "skateboard": [
        "A clean origami skateboard. It has a narrow board with four wheels attached, used for riding and performing tricks.",
        "A clean origami skateboard. It features a concave deck, grip tape on top, and trucks that connect the wheels.",
        "A clean origami skateboard. It displays a colorful graphic on the bottom, and small, hard wheels for smooth surfaces.",
        "A clean origami skateboard. It is characterized by a recreational and sports equipment for skateboarding.",
        "A clean origami skateboard. It shows a compact and portable design for urban transportation and stunts."
    ],
    "surfboard": [
        "A clean origami surfboard. It has a long, narrow board used for riding ocean waves, made of foam and fiberglass.",
        "A clean origami surfboard. It features a pointed nose, a rounded tail, and a fin or fins on the bottom.",
        "A clean origami surfboard. It displays a smooth, curved surface, a leash plug, and often a colorful design.",
        "A clean origami surfboard. It is characterized by a water sports equipment for surfing on waves.",
        "A clean origami surfboard. It shows a hydrodynamic shape that glides on water."
    ],
    "tennis racket": [
        "A clean origami tennis racket. It has an oval head with a stringed pattern, a handle, and a frame.",
        "A clean origami tennis racket. It features a grip at the handle, a throat connecting the head and handle, and a sweet spot.",
        "A clean origami tennis racket. It displays a lightweight construction, often made of graphite or aluminum, and a durable string bed.",
        "A clean origami tennis racket. It is characterized by a sports equipment used to hit a tennis ball.",
        "A clean origami tennis racket. It shows a symmetrical design and is swung with one hand or two."
    ],
    "bottle": [
        "A clean origami bottle. It has a cylindrical or curved body, a narrow neck, and a cap or cork for sealing.",
        "A clean origami bottle. It features a smooth glass or plastic surface, a label area on the front, and a flat base for stability.",
        "A clean origami bottle. It displays a transparent or colored material, a screw-top or flip-top lid, and often contains liquid.",
        "A clean origami bottle. It is characterized by a rounded shoulder near the neck and a cylindrical shape.",
        "A clean origami bottle. It shows a slender profile and a mouth opening for pouring."
    ],
    "wine glass": [
        "A clean origami wine glass. It has a stemmed glass with a bowl for holding wine, a stem, and a base.",
        "A clean origami wine glass. It features a delicate and elegant design, often made of clear glass, and a thin rim.",
        "A clean origami wine glass. It displays a tulip-shaped bowl, a long stem for holding, and a flat circular base.",
        "A clean origami wine glass. It is characterized by a drinking vessel used for serving wine.",
        "A clean origami wine glass. It shows a graceful shape that enhances the wine tasting experience."
    ],
    "cup": [
        "A clean origami cup. It has a small container with a handle, used for drinking hot or cold beverages.",
        "A clean origami cup. It features a cylindrical shape, a handle for gripping, and often made of ceramic or porcelain.",
        "A clean origami cup. It displays a simple design, a saucer sometimes accompanying it, and a decorative pattern.",
        "A clean origami cup. It is characterized by a common household item for serving drinks.",
        "A clean origami cup. It shows a functional and often decorative object."
    ],
    "fork": [
        "A clean origami fork. It has a handle and several tines (usually four) used for picking up food.",
        "A clean origami fork. It features a metal construction, a pointed end for spearing, and a comfortable grip.",
        "A clean origami fork. It displays a simple and utilitarian design, often part of a cutlery set.",
        "A clean origami fork. It is characterized by an eating utensil used in many cultures.",
        "A clean origami fork. It shows a basic yet essential tool for dining."
    ],
    "knife": [
        "A clean origami knife. It has a blade and a handle, used for cutting or spreading food.",
        "A clean origami knife. It features a sharp edge, a pointed tip, and a handle for safe gripping.",
        "A clean origami knife. It displays a simple design, often made of stainless steel, and a non-slip handle.",
        "A clean origami knife. It is characterized by a common kitchen and dining utensil.",
        "A clean origami knife. It shows a functional tool for preparing and eating meals."
    ],
    "dessertspoon": [
        "A clean origami dessertspoon. It has a small spoon with a bowl and a handle, used for eating desserts or soups.",
        "A clean origami dessertspoon. It features a rounded bowl, a comfortable handle, and often made of metal or plastic.",
        "A clean origami dessertspoon. It displays a simple and elegant design, smaller than a tablespoon but larger than a teaspoon.",
        "A clean origami dessertspoon. It is characterized by a versatile eating utensil for various courses.",
        "A clean origami dessertspoon. It shows a practical and common item in cutlery sets."
    ],
    "bowl": [
        "A clean origami bowl. It has a round, deep dish used for serving food like soup, cereal, or salad.",
        "A clean origami bowl. It features a curved interior, a flat or footed base, and often made of ceramic or glass.",
        "A clean origami bowl. It displays a simple and functional design, sometimes with a lip or handle.",
        "A clean origami bowl. It is characterized by a common kitchenware item for holding food.",
        "A clean origami bowl. It shows a hemispherical shape that holds liquids and solids."
    ],
    "banana": [
        "A clean origami banana. It has a curved yellow fruit with a peel that is removed to eat the soft inside.",
        "A clean origami banana. It features a long, slightly arched shape, a stem at one end, and a tip at the other.",
        "A clean origami banana. It displays a smooth skin that turns from green to yellow as it ripens.",
        "A clean origami banana. It is characterized by a tropical fruit that is a popular snack.",
        "A clean origami banana. It shows a simple and recognizable fruit shape."
    ],
    "apple": [
        "A clean origami apple. It has a round fruit with a stem at the top and a calyx at the bottom, often red or green.",
        "A clean origami apple. It features a smooth skin, a core inside with seeds, and a juicy flesh.",
        "A clean origami apple. It displays a symmetrical shape, a small dimple at the base, and sometimes a shiny appearance.",
        "A clean origami apple. It is characterized by a common fruit that is eaten raw or used in cooking.",
        "A clean origami apple. It shows a classic fruit shape that is widely recognized."
    ],
    "sandwich": [
        "A clean origami sandwich. It has two slices of bread with fillings such as meat, cheese, or vegetables in between.",
        "A clean origami sandwich. It features a layered structure, often cut into halves or triangles, and held together.",
        "A clean origami sandwich. It displays a variety of ingredients visible from the side, and a soft or toasted bread exterior.",
        "A clean origami sandwich. It is characterized by a popular meal item that is portable and customizable.",
        "A clean origami sandwich. It shows a simple yet versatile food item."
    ],
    "orange": [
        "A clean origami orange. It has a round citrus fruit with a bright orange peel that is often peeled to reveal segments.",
        "A clean origami orange. It features a dimpled skin, a small stem at one end, and a juicy interior.",
        "A clean origami orange. It displays a spherical shape, a thick rind, and a vibrant color.",
        "A clean origami orange. It is characterized by a vitamin-rich fruit commonly eaten fresh or juiced.",
        "A clean origami orange. It shows a simple and round fruit with a textured surface."
    ],
    "broccoli": [
        "A clean origami broccoli. It has a green vegetable with a tree-like shape, consisting of a stalk and florets.",
        "A clean origami broccoli. It features a thick stem and branching clusters of dark green buds.",
        "A clean origami broccoli. It displays a natural, fractal-like appearance and a rough texture.",
        "A clean origami broccoli. It is characterized by a nutritious vegetable often steamed or stir-fried.",
        "A clean origami broccoli. It shows a distinctive shape that resembles a small tree."
    ],
    "carrot": [
        "A clean origami carrot. It has a long, conical root vegetable with a bright orange color and a green top.",
        "A clean origami carrot. It features a smooth skin, a tapered shape, and a crisp texture when fresh.",
        "A clean origami carrot. It displays a simple and elongated form, often with ridges and a pointed tip.",
        "A clean origami carrot. It is characterized by a common vegetable that is eaten raw or cooked.",
        "A clean origami carrot. It shows a slender and tapered root shape."
    ],
    "hot dog": [
        "A clean origami hot dog. It has a cooked sausage placed inside a long, soft bun, often with toppings.",
        "A clean origami hot dog. It features a cylindrical meat product, a split bun, and condiments like ketchup or mustard.",
        "A clean origami hot dog. It displays a simple and portable food item, often associated with casual dining.",
        "A clean origami hot dog. It is characterized by a popular fast food item at sporting events and barbecues.",
        "A clean origami hot dog. It shows a basic yet iconic sandwich-like food."
    ],
    "pizza": [
        "A clean origami pizza. It has a round, flat base of dough topped with tomato sauce, cheese, and various toppings.",
        "A clean origami pizza. It features a circular shape, often sliced into triangular pieces, and a baked crust.",
        "A clean origami pizza. It displays a colorful array of toppings such as pepperoni, vegetables, or mushrooms.",
        "A clean origami pizza. It is characterized by a popular Italian dish that is enjoyed worldwide.",
        "A clean origami pizza. It shows a round, flat food item that is typically shared."
    ],
    "donut": [
        "A clean origami donut. It has a ring-shaped pastry made of fried dough, often coated with sugar or glaze.",
        "A clean origami donut. It features a circular shape with a hole in the center, and a soft, fluffy texture.",
        "A clean origami donut. It displays a sweet coating, such as chocolate or sprinkles, and a golden-brown color.",
        "A clean origami donut. It is characterized by a popular sweet treat often eaten for breakfast or dessert.",
        "A clean origami donut. It shows a simple and recognizable shape that is enjoyed by many."
    ],
    "cake": [
        "A clean origami cake. It has a baked dessert made from flour, sugar, and eggs, often layered and frosted.",
        "A clean origami cake. It features a soft and spongy texture, a sweet frosting, and sometimes decorative elements.",
        "A clean origami cake. It displays a rectangular or round shape, and is often served on special occasions.",
        "A clean origami cake. It is characterized by a celebratory dessert that comes in many flavors and styles.",
        "A clean origami cake. It shows a layered and frosted appearance that is visually appealing."
    ],
    "chair seat": [
        "A clean origami chair seat. It has a flat horizontal seat surface, a vertical backrest, and four legs for support.",
        "A clean origami chair seat. It features a simple rectangular or curved design, often made of wood or plastic.",
        "A clean origami chair seat. It displays armrests on the sides, a cushioned seat, and sometimes wheels on the legs.",
        "A clean origami chair seat. It is characterized by a sturdy frame and a slatted or upholstered back.",
        "A clean origami chair seat. It shows a functional structure and a seat height suitable for sitting at a table."
    ],
    "sofa": [
        "A clean origami sofa. It has a long cushioned seat for multiple people, a backrest, and armrests on both ends.",
        "A clean origami sofa. It features an upholstered surface in fabric or leather and often includes throw pillows.",
        "A clean origami sofa. It displays a sturdy wooden or metal frame underneath and a padded seat.",
        "A clean origami sofa. It is characterized by a rectangular shape and a seat height lower than a chair.",
        "A clean origami sofa. It shows a cohesive design and seams or buttons on the surface."
    ],
    "pottedplant": [
        "A clean origami pottedplant. It has a container or pot holding soil with green leaves or stems growing upward.",
        "A clean origami pottedplant. It features a central stem or multiple branches and leaves that may be broad or narrow.",
        "A clean origami pottedplant. It displays a simple decorative pot often in terracotta or ceramic.",
        "A clean origami pottedplant. It is characterized by a compact growth habit and a root system hidden inside the pot.",
        "A clean origami pottedplant. It shows a natural green color and a pot with a drainage hole."
    ],
    "bed": [
        "A clean origami bed. It has a large rectangular frame with a mattress, used for sleeping or resting.",
        "A clean origami bed. It features a headboard, a footboard, and a supportive base, often with sheets and pillows.",
        "A clean origami bed. It displays a comfortable and inviting appearance, and is a central piece in bedrooms.",
        "A clean origami bed. It is characterized by a piece of furniture designed for sleeping.",
        "A clean origami bed. It shows a simple yet essential household item."
    ],
    "diningtable": [
        "A clean origami diningtable. It has a flat rectangular or round top surface supported by four legs.",
        "A clean origami diningtable. It features a smooth tabletop often made of wood or glass and a central pedestal.",
        "A clean origami diningtable. It displays a sturdy construction and a surface for placing plates and utensils.",
        "A clean origami diningtable. It is characterized by a polished finish and a uniform height suitable for chairs.",
        "A clean origami diningtable. It shows a simple geometric design and edges that may be rounded or straight."
    ],
    "toilet": [
        "A clean origami toilet. It has a porcelain fixture with a seat and a lid, used for human waste disposal.",
        "A clean origami toilet. It features a water tank, a bowl, and a flushing mechanism, and is often white.",
        "A clean origami toilet. It displays a simple and functional design, typically found in bathrooms.",
        "A clean origami toilet. It is characterized by a sanitary ware essential in modern plumbing.",
        "A clean origami toilet. It shows a recognizable shape with a seat and a tank."
    ],
    "tvmonitor screen": [
        "A clean origami tvmonitor screen. It has a flat rectangular screen, a bezel around the edges, and a stand or wall mount.",
        "A clean origami tvmonitor screen. It features a black or dark frame and a smooth glass surface.",
        "A clean origami tvmonitor screen. It displays a thin profile and control buttons or ports on the side.",
        "A clean origami tvmonitor screen. It is characterized by a widescreen aspect ratio and a glossy or matte finish.",
        "A clean origami tvmonitor screen. It shows a simple geometric shape and a screen that may be on or off."
    ],
    "laptop": [
        "A clean origami laptop. It has a clamshell design with a screen and a keyboard, used for portable computing.",
        "A clean origami laptop. It features a thin profile, a trackpad, and various ports for connectivity.",
        "A clean origami laptop. It displays a sleek metal or plastic casing, and a brand logo on the lid.",
        "A clean origami laptop. It is characterized by a personal computer that folds for transportation.",
        "A clean origami laptop. It shows a rectangular shape when closed and opens to reveal the screen and keyboard."
    ],
    "mouse": [
        "A clean origami mouse. It has a small handheld device with buttons and a scroll wheel, used to control a computer cursor.",
        "A clean origami mouse. It features an ergonomic shape that fits in the hand, and a cable or wireless connection.",
        "A clean origami mouse. It displays a simple design with left and right buttons, and often a LED light on the bottom.",
        "A clean origami mouse. It is characterized by a common computer peripheral for navigation.",
        "A clean origami mouse. It shows a compact and curved shape designed for hand comfort."
    ],
    "remote control": [
        "A clean origami remote control. It has a rectangular handheld device with buttons for operating electronic devices.",
        "A clean origami remote control. It features a simple layout, often with a directional pad and numeric buttons.",
        "A clean origami remote control. It displays a plastic casing, an infrared transmitter, and sometimes a brand logo.",
        "A clean origami remote control. It is characterized by a device used to control TVs, stereos, or other appliances.",
        "A clean origami remote control. It shows a small, rectangular shape that fits in the hand."
    ],
    "keyboard": [
        "A clean origami keyboard. It has a set of keys arranged in rows, used for typing on a computer or other device.",
        "A clean origami keyboard. It features alphanumeric keys, function keys, and a QWERTY layout.",
        "A clean origami keyboard. It displays a rectangular shape, often with a numeric keypad on the right, and a wired or wireless connection.",
        "A clean origami keyboard. It is characterized by an input device for computers and typewriters.",
        "A clean origami keyboard. It shows a flat and wide design with many small, square keys."
    ],
    "cell phone": [
        "A clean origami cell phone. It has a small handheld device with a screen and buttons or touch interface, used for communication.",
        "A clean origami cell phone. It features a rectangular shape, a camera lens, and often a brand logo on the back.",
        "A clean origami cell phone. It displays a sleek design, a charging port, and a speaker grille.",
        "A clean origami cell phone. It is characterized by a portable telephone that can also run applications.",
        "A clean origami cell phone. It shows a compact and flat device that fits in the palm of the hand."
    ],
    "microwave": [
        "A clean origami microwave. It has a box-shaped appliance with a door, used for heating food quickly.",
        "A clean origami microwave. It features a control panel, a rotating turntable inside, and a handle to open the door.",
        "A clean origami microwave. It displays a simple and functional design, often in white or stainless steel.",
        "A clean origami microwave. It is characterized by a common kitchen appliance for reheating meals.",
        "A clean origami microwave. It shows a rectangular box with a glass window on the front."
    ],
    "oven": [
        "A clean origami oven. It has a enclosed cooking chamber with a door, used for baking or roasting food.",
        "A clean origami oven. It features a control panel, heating elements, and a window to view the interior.",
        "A clean origami oven. It displays a rectangular shape, often built into a kitchen cabinet or freestanding.",
        "A clean origami oven. It is characterized by a major kitchen appliance for cooking.",
        "A clean origami oven. It shows a simple and sturdy design with a hinged door."
    ],
    "toaster": [
        "A clean origami toaster. It has a small appliance with slots for inserting bread, used to toast it with heat.",
        "A clean origami toaster. It features a lever to lower the bread, a timer dial, and often a cancel button.",
        "A clean origami toaster. It displays a compact design, often in chrome or colored plastic, and a crumb tray.",
        "A clean origami toaster. It is characterized by a common kitchen gadget for making toast.",
        "A clean origami toaster. It shows a simple rectangular shape with two or four slots on top."
    ],
    "sink": [
        "A clean origami sink. It has a basin with a faucet, used for washing hands, dishes, or food.",
        "A clean origami sink. It features a drain, a water tap, and often a countertop or cabinet underneath.",
        "A clean origami sink. It displays a simple and functional design, often made of stainless steel or porcelain.",
        "A clean origami sink. It is characterized by a plumbing fixture found in kitchens and bathrooms.",
        "A clean origami sink. It shows a bowl-shaped basin with a faucet above."
    ],
    "refrigerator": [
        "A clean origami refrigerator. It has a large appliance with a door, used to keep food cold and fresh.",
        "A clean origami refrigerator. It features a freezer compartment, shelves inside, and often an ice maker.",
        "A clean origami refrigerator. It displays a rectangular shape, a handle to open the door, and a brand logo.",
        "A clean origami refrigerator. It is characterized by an essential kitchen appliance for food storage.",
        "A clean origami refrigerator. It shows a tall and boxy design with a smooth exterior."
    ],
    "book": [
        "A clean origami book. It has a set of printed pages bound together between two covers.",
        "A clean origami book. It features a spine, a front and back cover, and often a title on the front.",
        "A clean origami book. It displays a rectangular shape, a variable thickness, and pages that turn.",
        "A clean origami book. It is characterized by a source of information or entertainment in written form.",
        "A clean origami book. It shows a simple yet iconic object found in homes and libraries."
    ],
    "clock": [
        "A clean origami clock. It has a circular or square face with numbers and hands to show the time.",
        "A clean origami clock. It features a simple design, often hung on a wall or placed on a surface.",
        "A clean origami clock. It displays an analog or digital display, and a mechanism for keeping time.",
        "A clean origami clock. It is characterized by a timekeeping device found in many rooms.",
        "A clean origami clock. It shows a familiar object that helps people manage their schedules."
    ],
    "vase": [
        "A clean origami vase. It has a container with an open top, used to hold cut flowers or as a decoration.",
        "A clean origami vase. It features a curved shape, a narrow neck, and often made of glass or ceramic.",
        "A clean origami vase. It displays a simple and elegant design, sometimes with patterns or colors.",
        "A clean origami vase. It is characterized by a decorative item often placed on tables or shelves.",
        "A clean origami vase. It shows a graceful form that enhances the beauty of flowers."
    ],
    "scissors": [
        "A clean origami scissors. It has two blades pivoted together, used for cutting paper, fabric, or other materials.",
        "A clean origami scissors. It features handles with finger holes, a sharp cutting edge, and a screw or rivet.",
        "A clean origami scissors. It displays a simple and functional design, often made of metal and plastic.",
        "A clean origami scissors. It is characterized by a common tool found in homes and offices.",
        "A clean origami scissors. It shows a recognizable shape with two blades and two handles."
    ],
    "teddy bear": [
        "A clean origami teddy bear. It has a stuffed toy in the shape of a bear, often with soft fur and friendly features.",
        "A clean origami teddy bear. It features a rounded body, arms and legs, and often a ribbon or bow.",
        "A clean origami teddy bear. It displays a cute and cuddly appearance, with eyes, a nose, and a mouth.",
        "A clean origami teddy bear. It is characterized by a popular children's toy that provides comfort.",
        "A clean origami teddy bear. It shows a simple and lovable shape that is cherished by many."
    ],
    "hairdrier,blowdrier": [
        "A clean origami hairdrier,blowdrier. It has a handheld device with a nozzle and a handle, used to dry hair with hot air.",
        "A clean origami hairdrier,blowdrier. It features a motor, a heating element, and often multiple speed and heat settings.",
        "A clean origami hairdrier,blowdrier. It displays a simple and ergonomic design, with a cord for electricity.",
        "A clean origami hairdrier,blowdrier. It is characterized by a common personal care appliance.",
        "A clean origami hairdrier,blowdrier. It shows a recognizable shape with a nozzle and a handle."
    ],
    "toothbrush": [
        "A clean origami toothbrush. It has a small brush with bristles on a handle, used for cleaning teeth.",
        "A clean origami toothbrush. It features a long, narrow handle and a head with tightly packed bristles.",
        "A clean origami toothbrush. It displays a simple and functional design, often in bright colors.",
        "A clean origami toothbrush. It is characterized by a personal hygiene item used daily.",
        "A clean origami toothbrush. It shows a slender and elongated shape with a brush head."
    ]
}