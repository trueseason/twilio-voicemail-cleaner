# twilio-voicemail-cleaner

This repository is a sample function of deleting Twilio voicemails based on the dates specified.

It is similar to the related functions in the package from Twilio, but more powerful (**and more dangerous**) as it could delete all the voicemails from a given date, all earlier dates, or all later dates. So it is possible to delete all voicemails in one call.



### Function

`def delete_voicemails_by_date(self, date_created, filter=DateFilter.EXACT_DATE_ONLY, recordLimit=10000)`

```
DateFilter Enum:
    EXACT_DATE_ONLY = 1
    INCLUDE_EARLIER_DATES = 2
    INCLUDE_LATER_DATES = 3
```



### Usage

```
from voicemail import Voicemail, DateFilter

vm = Voicemail("twilioAccountId", "twilioAuthToken")
vm.delete_voicemails_by_date(datetime.datetime(2010,01,31))
```

