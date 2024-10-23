CREATE TABLE Inventory(
	InventoryID bigint NOT NULL,
	InventoryBatchID bigint NOT NULL,
	ReportDate date NOT NULL,
	LoanID varchar(40) NOT NULL,
	WarehouseLineID bigint NOT NULL,
	UnpaidPrincipleBalance decimal(18, 2) NOT NULL,
	AdvanceAmount decimal(18, 2) NOT NULL,
	FundDate date NOT NULL,
	Age int NOT NULL,
	Interest decimal(18, 2) NOT NULL,
	CollateralType VARCHAR(100) NOT NULL,
	Category VARCHAR(100) NULL,
	LoanType VARCHAR(100) NOT NULL,
	UpdateDateTime datetime NOT NULL,
	UpdatedBy varchar(200) NOT NULL
);


CREATE TABLE WarehouseLine(
	WarehouseLineID bigint  NOT NULL,
	WarehouseLineName VARCHAR(100) NULL,
	Originator varchar(40) NULL,
	Capacity decimal(18, 1) NULL,
	CommittedCapacity decimal(18, 1) NULL,
	UncommittedCapacity decimal(18, 1) NULL,
	Sublimit decimal(18, 1) NULL,
	NonUsageThreshold decimal(18, 1) NULL
);


CREATE TABLE REPORTING_LOANS (
    PoolNbr VARCHAR(200) NULL,
    SettlementNbr VARCHAR(200) NULL,
    SoldTo VARCHAR(200) NULL,
    LoanID BIGINT NULL,
    FacilityName VARCHAR(200) NULL,
    FacilityID INT NULL,
    WarehouseID INT NULL,
    WarehouseName VARCHAR(200) NULL,
    WarehouseDate DATETIME NULL,
    FacilityDate DATETIME NULL,
    OriginalFacilityDate DATETIME NULL,
    BankingPackageReceivedDate DATETIME NULL,
    ShippedDate DATETIME NULL,
    SettlementDate DATETIME NULL,
    Comments VARCHAR(2000) NULL,
    UserField1 VARCHAR(200) NULL,
    UserField2 VARCHAR(200) NULL,
    AdvanceRate DECIMAL(6, 3) NULL,
    CalculatedAdvanceAmount DECIMAL(18,2) NULL,
    AdvanceAmount DECIMAL(18,2) NULL,
    WireValueDate DATETIME NULL,
    NoteDate DATETIME NULL,
    NextPaymentDueDate DATETIME NULL,
    FirstPaymentDueDate DATETIME NULL,
    CloseDate DATETIME NULL,
    RefiCode VARCHAR(4) NULL,
    NumberOfUnits INT NULL,
    NextRateChange DATETIME NULL,
    AmortizationType DECIMAL(5, 0) NULL,
    InterestOnlyPeriod DECIMAL(5, 3) NULL,
    PaidOff VARCHAR(200) NULL,
    TakeoutPrice DECIMAL(19, 2) NULL,
    CurrentUPB DECIMAL(18,2) NOT NULL,
    OriginalUPB DECIMAL(18,2) NOT NULL,
    BorrowerLastName VARCHAR(80) NOT NULL,
    Program VARCHAR(24) NOT NULL,
    Product VARCHAR(16) NOT NULL,
    InterestRate DECIMAL(6, 3) NOT NULL,
    LTV DECIMAL(5, 2) NOT NULL,
    CLTV DECIMAL(5, 2) NOT NULL,
    Term DECIMAL(4, 0) NOT NULL,
    FICO INT NOT NULL,
    LienPosition INT NOT NULL,
    IsOwnerOccupied INT NULL,
    IsTexasCashOutRefinance INT NULL,
    DocumentationType DECIMAL(1, 0) NULL,
    PropertyType DECIMAL(2, 0) NULL,
    IsWet INT NOT NULL
);