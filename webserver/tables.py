from enum import Enum
tables = {}
tables['Accounts'] = (
    '`Accounts` ('
    '`UserID` int NOT NULL AUTO_INCREMENT,'
    '`UserName` varchar(20) NOT NULL,'
    '`Email` varchar(45) NOT NULL,'
    '`Password` varchar(50) NOT NULL,'
    '`AccessLevel` varchar(10) DEFAULT NULL,'
    'PRIMARY KEY (`UserID`),'
    'UNIQUE KEY `UserName_UNIQUE` (`UserName`),'
    'UNIQUE KEY `E-mail_UNIQUE` (`Email`)'
    ')ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci')

tables['Products'] = (
    '`Products` ('
    '`ProductID` int NOT NULL AUTO_INCREMENT,'
    '`Name` varchar(45) NOT NULL,'
    '`Make` varchar(45) NOT NULL,'
    '`Price` int NOT NULL,'
    '`InStock` int NOT NULL,'
    '`Image` varchar(45) DEFAULT NULL,'
    'PRIMARY KEY (`ProductID`),'
    'UNIQUE KEY `MAKE_NAME` (`Name`,`Make`)'
    ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'
    )

tables['Transactions'] = (
    '`Transactions` ('
    '`TransactionNumber` int NOT NULL AUTO_INCREMENT,'
    '`UserID` int NOT NULL,'
    '`DateTime` date DEFAULT NULL,'
    '`Status` varchar(20) NOT NULL,'
    'PRIMARY KEY (`TransactionNumber`),'
    'KEY `UserID_idx` (`UserID`),'
    'CONSTRAINT `UserID` FOREIGN KEY (`UserID`) REFERENCES `Accounts` (`UserID`)'
    ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'
    )

tables['TransactionData'] = (
    '`TransactionData` ('
    '`TransactionNumber` int NOT NULL,'
    '`Item` int NOT NULL,'
    '`Count` int NOT NULL,'
    'KEY `TransactionNumber_idx` (`TransactionNumber`),'
    'KEY `ProductId_idx` (`Item`),'
    'CONSTRAINT `ProductIdData` FOREIGN KEY (`Item`) REFERENCES `Products` (`ProductID`),'
    'CONSTRAINT `TransactionNumberData` FOREIGN KEY (`TransactionNumber`) REFERENCES `Transactions` (`TransactionNumber`)'
    ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'
    )


transaction = (
    '`Transaction%(UserID)s` ('
    '`TransactionNumber` int NOT NULL,'
    '`Item` int NOT NULL,'
    '`Count` int NOT NULL,'
    'KEY `TransactionNumber_idx` (`TransactionNumber`),'
    'KEY `ProductId_idx` (`Item`),'
    'CONSTRAINT `ProductId%(UserID)s` FOREIGN KEY (`Item`) REFERENCES `Products` (`ProductID`),'
    'CONSTRAINT `TransactionNumber%(UserID)s` FOREIGN KEY (`TransactionNumber`) REFERENCES `Transactions` (`TransactionNumber`)'
    ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'
    )



accountsInsert = 'Accounts (UserName, Email, Password, AccessLevel)'
productsInsert = 'Products (Name, Make, Price,  InStock)'
productsInsertImage = 'Products (Name, Make, Price,  InStock, Image)'
transactionsInsert = 'Transactions (UserID, Status)'
transactionDataInsert = 'TransactionData (TransactionNumber, Item, Count)'


class TransactionState(Enum):
    DONE = "completed"
    WAIT = "inprogress"
    BASKET = "inbasket"
