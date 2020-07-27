# MySignalsLib

This is a python library for **MySignals SW: eHealth IoT Development platform**. It makes the interaction with the MySignals Cloud REST API easier for the end user.

## Example Usage:

 **Create mysignals object:**
 
```
mysig = mysignals(username = "Your username for MySignals Cloud" , password = "Your password for MySignals Cloud")
```

 **Get available members:**
 
```
members = mysig.get_members()
```

or you can access that list from:
```
mysig.members
```

 **Update the members list:**
 
```
mysig.update_members()
```


 **Update the status of a member(Active = Retrieve data for that member):**
 
```
mysig.change_status(member_id="member id of member of interest", status=1) // To set that member to Active
```

 **Check if someone is a member:**
 
```
mysig.is_member(member_id="member id of member of interest", name="Name of member of interest" surname="Surname of member of interest") // Returns True if the person is in the member list
```

 **Add a sensor to a member's sensor's list:**
 
```
mysig.add_sensor(sensor_id="sensor id of sensor to add", member_id="member id of member of interest")
```

 **Remove a sensor from a member's sensor's list:**
 
```
mysig.remove_sensor(sensor_id="sensor id of sensor to remove", member_id="member id of member of interest")
```

**Get the values from a specific sensor of a specific member for a specific time horizon:**
 
```
mysig.values(sensor_id="sensor of interest",member_id="member of interest" ,ts_start="end date of the range that the data will retrieved for",ts_end="starting date of the range that the data will retrieved for",limit="Number of values to retrieve",order="desc")
```

**Get continues raw values from a specific sensor for a specific member for a specific time horizon:**
 
```
mysig.raws(sensor_id="sensor of interest",member_id="member of interest" ,ts_start="end date of the range that the data will retrieved for",ts_end="starting date of the range that the data will retrieved for")
```


**Get the latest values of the sensors of a specific member:**
 
```
mysig.live(sensor_id="sensor of interest",member_id="member of interest" ,ts_start="end date of the range that the data will retrieved for",ts_end="starting date of the range that the data will retrieved for")
```

Sensor values are saved in **sensor_value** and **sensor_raws**. Both have the same attributes as their respecting counterparts on the REST API.

### For example:

```
sv = mysig.sensor_value()

sv.value

srv = mysig.sensor_raws()

srv.parts_total
```

Reference: http://www.my-signals.com/






