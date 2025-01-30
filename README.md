# LISMS
Labratory Inventory &amp; Sample Managamenet System (LISMS) is a database that can keep track of pharmaceutical laboratory inventory (reagents and other chemicals) and samples (multiple types of drug samples) in order to ensure everything is stored properly and inventory is maintained ahead of time so testing is not affected. Eventually, I'll add audit functionality so whenever inventory, samples, or tests are altered in any way, an audit comment would be required of the user to maintain transparency and accountability. I'll also be adding a frontend to this project to make the UI easier to understand and use by the typical consumer. For now, the database is functional with keeping track of both sample and inventory storage locations, sample test dates, test results, etc. To launch this file, you need to have Microsoft SQL Server Management Studio (an EDMS) to open the file and launch it. The file also contains procedures for easy initialization of the tables for testing purposes. The database has been normalized and indexing and sequencing have been utilized as well to improve efficiency, ease of use, and prevent primary key errors (overlapping PKs).
