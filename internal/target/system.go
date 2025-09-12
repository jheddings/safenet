package target

type SystemTarget struct {
	Name    string
	Address string
	Safe    bool
}

func (t *SystemTarget) Check() (bool, error) {
	return true, nil
}
