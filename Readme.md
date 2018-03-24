This is a collection of scripts that convert various object detection formats to the Pascal VOC format. The VOC format was chosen because extra data from each format can be added to the xml file. 

The goal is to have converters for:
- [x] KITTI
- [x] Udacity Crowd AI
- [x] Udacity Autti
- [x] MIT Street Scenes

The data from each format will be converted to Pascal VOC format with additional tags to hold the format specific data. A "converter" tag will be added to each file with information about how/when the data was converted.

Every file must have the following information. Other information is allowed as well:

| Tag 1  | Tag 2 | Tag 3 | Description |
| --- | --- | --- | --- |
| annotation |   |   |   |
|   | folder |   |   |  folder where the image is stored, relative to top level | 
|   | filename|   |   | filename of the image, no path included |
|   | source |   |   |   |
|   |   | database | The database name the image is from  |
| size |  |  |  |
|  | width |  | width of image in pixels |
|  | height |  | height of image in pixels |
|  | depth |  | number of color channels |
| object |  |  |  |
|  | name |  | plain text name of the object |
|  | bndbox |  |  |
|  |  | xmin | left location of bounding box, is float |
|  |  | ymin | top location of bounding box, is float |
|  |  | xmax | right location of bounding box, is float |
|  |  | ymax | botom location of bounding box, is float |
| conversion |  |  |  |
|  | created |  | the date this file was created, yyyy-mm-ddThh:mm:ss.ffff |
|  | updated |  | the date this file was updated, yyyy-mm-ddThh:mm:ss.ffff |
|  |  |  |  |


The basic code breakdown is:
* Every converter is inherited from the VOCConverter which defines some basics about what every label file must have
* There is a converter for each dataset that implements how to:
* * Iterate through every image and label
* * Convert each label to VOC format

Because these files only need to be converted once, the paths are hard coded at the top of each script.