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